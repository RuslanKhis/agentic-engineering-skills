#!/usr/bin/env python3
"""Compare two versions of an agent on the same cases: paired difference, interval and sample size. Standard library only.

Reads two trial records, ``--baseline`` and ``--candidate``, CSV or JSON Lines,
one row per trial. Each row needs ``case_id`` and a score: ``reward`` or
``score`` (a finite number, higher is better), or else ``outcome`` (``pass``
counts 1, ``fail`` 0). A row whose ``outcome`` is ``infra_error`` is left out
of the figures and counted. Optional fields: ``scenario`` (cases that are
variants of one scenario share it, and the standard error is clustered on
it) and ``trial_id`` (a repeated ID in one file is an error).

Method (Evan Miller, "Adding Error Bars to Evals", arXiv 2411.00640): a case's
runs are averaged first, so K runs of one case count once, never as K
independent samples. The difference is taken per case (candidate minus
baseline) and averaged. Its standard error is clustered on the scenario, or
on the case when there is no scenario column, with the small-sample factor
G/(G-1) for G clusters; the interval uses Student's t with G-1 degrees of
freedom. The minimum detectable difference is (t[alpha/2] + t[power]) x SE:
a true difference that size is found with the stated power, and a smaller
observed move is within noise. With ``--target-difference`` it also reports
how many cases would detect that difference, from the variance measured
here: n = (z[alpha/2] + z[power])^2 x V / d^2 (refined with t for small n),
where V is the per-case variance of the difference; with ``--plan-cases N``
it reports the difference N cases could detect (a holdout a budget buys).
Plans count scenarios as the unit and keep this sample's cases per scenario.
When cases ran more than once, V is split into between-case variance and
run-to-run noise, so ``--plan-runs K`` can show the same at K runs per case;
on a small sample the noise estimate can exceed V, and then the split is
reported as not estimable.

Verdict: ``improved`` when the interval lies above zero, ``worse`` when it
lies below, otherwise ``within noise``. ``--require improved`` exits 1
unless the verdict is ``improved``; ``--require not-worse --margin M`` exits
1 unless the interval's lower end is above -M (a cheaper model or a refactor
that must not lose more than M).

Exit status: 0 computed (and any --require met), 1 a --require not met,
2 unreadable or invalid input, 3 incomplete: a case has scores in one file
only, or too few cases or scenarios to estimate an interval, so the figures
printed may change once the missing cases run.
"""

from __future__ import annotations

import argparse
import csv
import io
import json
import math
from pathlib import Path
import sys
from statistics import NormalDist

MAX_BYTES = 20 * 1024 * 1024
MAX_PLAN_CASES = 10_000_000
OK, NOT_MET, BAD_INPUT, INCOMPLETE = 0, 1, 2, 3


class InputError(Exception):
    pass


# ---------------------------------------------------------------- reading


def read_rows(path: Path) -> list[dict]:
    try:
        if path.stat().st_size > MAX_BYTES:
            raise InputError(f"{path}: larger than {MAX_BYTES // (1024 * 1024)} MB")
        text = path.read_text(encoding="utf-8-sig")
    except (OSError, UnicodeError) as exc:
        raise InputError(f"{path}: cannot read: {exc}") from exc
    rows = []
    if path.suffix.lower() in (".jsonl", ".ndjson") or text.lstrip().startswith("{"):
        for number, line in enumerate(text.splitlines(), start=1):
            if not line.strip():
                continue
            try:
                row = json.loads(line)
            except json.JSONDecodeError as exc:
                raise InputError(f"{path}:{number}: not JSON: {exc.msg}") from exc
            if not isinstance(row, dict):
                raise InputError(f"{path}:{number}: a row must be a JSON object")
            rows.append(row)
    else:
        reader = csv.DictReader(io.StringIO(text))
        if not reader.fieldnames or "case_id" not in reader.fieldnames:
            raise InputError(f"{path}: the CSV header has no case_id column")
        rows = list(reader)
    if not rows:
        raise InputError(f"{path}: no rows")
    return rows


def score_of(row: dict, where: str) -> float | None:
    """The row's score, or None for an infrastructure error."""
    outcome = str(row.get("outcome") or "").strip().lower()
    if outcome == "infra_error":
        return None
    for field in ("reward", "score"):
        value = row.get(field)
        if value is not None and str(value).strip() != "":
            try:
                number = float(value)
            except (TypeError, ValueError) as exc:
                raise InputError(f"{where}: {field} is not a number") from exc
            if not math.isfinite(number):
                raise InputError(f"{where}: {field} is not finite")
            return number
    if outcome in ("pass", "fail"):
        return 1.0 if outcome == "pass" else 0.0
    raise InputError(f"{where}: no reward, score or pass/fail outcome")


def load_arm(path: Path) -> tuple[dict[str, list[float]], dict[str, str], int]:
    """Scores per case, scenario per case, and the count of infra_error rows."""
    scores: dict[str, list[float]] = {}
    scenarios: dict[str, str] = {}
    trial_ids: set[str] = set()
    infra = 0
    for number, row in enumerate(read_rows(path), start=1):
        where = f"{path} row {number}"
        case = str(row.get("case_id") or "").strip()
        if not case:
            raise InputError(f"{where}: empty case_id")
        trial = str(row.get("trial_id") or "").strip()
        if trial:
            if trial in trial_ids:
                raise InputError(f"{where}: trial_id {trial!r} repeated")
            trial_ids.add(trial)
        scenario = str(row.get("scenario") or "").strip()
        if scenario:
            if scenarios.setdefault(case, scenario) != scenario:
                raise InputError(f"{where}: case {case!r} has two scenarios")
        value = score_of(row, where)
        if value is None:
            infra += 1
            scores.setdefault(case, [])
            continue
        scores.setdefault(case, []).append(value)
    return scores, scenarios, infra


# ---------------------------------------------------------- distributions


def _betacf(a: float, b: float, x: float) -> float:
    """Continued fraction for the incomplete beta function (modified Lentz)."""
    tiny = 1e-300
    qab, qap, qam = a + b, a + 1.0, a - 1.0
    c, d = 1.0, 1.0 - qab * x / qap
    d = 1.0 / (d if abs(d) > tiny else tiny)
    h = d
    for m in range(1, 300):
        m2 = 2 * m
        aa = m * (b - m) * x / ((qam + m2) * (a + m2))
        d = 1.0 + aa * d
        d = 1.0 / (d if abs(d) > tiny else tiny)
        c = 1.0 + aa / c
        c = c if abs(c) > tiny else tiny
        h *= d * c
        aa = -(a + m) * (qab + m) * x / ((a + m2) * (qap + m2))
        d = 1.0 + aa * d
        d = 1.0 / (d if abs(d) > tiny else tiny)
        c = 1.0 + aa / c
        c = c if abs(c) > tiny else tiny
        delta = d * c
        h *= delta
        if abs(delta - 1.0) < 1e-14:
            break
    return h


def _betainc(a: float, b: float, x: float) -> float:
    """Regularised incomplete beta I_x(a, b)."""
    if x <= 0.0:
        return 0.0
    if x >= 1.0:
        return 1.0
    front = math.exp(math.lgamma(a + b) - math.lgamma(a) - math.lgamma(b)
                     + a * math.log(x) + b * math.log(1.0 - x))
    if x < (a + 1.0) / (a + b + 2.0):
        return front * _betacf(a, b, x) / a
    return 1.0 - front * _betacf(b, a, 1.0 - x) / b


def t_cdf(t: float, df: float) -> float:
    tail = 0.5 * _betainc(df / 2.0, 0.5, df / (df + t * t))
    return 1.0 - tail if t >= 0 else tail


def t_quantile(p: float, df: float) -> float:
    """Student's t quantile for 0.5 <= p < 1, by bisection on the CDF."""
    if df > 1e6:
        return NormalDist().inv_cdf(p)
    low, high = 0.0, 1.0
    while t_cdf(high, df) < p:
        high *= 2.0
    for _ in range(200):
        mid = (low + high) / 2.0
        if t_cdf(mid, df) < p:
            low = mid
        else:
            high = mid
    return (low + high) / 2.0


# ------------------------------------------------------------ statistics


def clustered_se(values: dict[str, float], cluster_of: dict[str, str]) -> tuple[float, int]:
    """SE of the mean of per-case values, clustered, with the G/(G-1) factor."""
    n = len(values)
    mean = sum(values.values()) / n
    sums: dict[str, float] = {}
    for case, value in values.items():
        key = cluster_of.get(case, case)
        sums[key] = sums.get(key, 0.0) + (value - mean)
    g = len(sums)
    if g < 2:
        return math.nan, g
    total = sum(s * s for s in sums.values())
    return math.sqrt(g / (g - 1) * total) / n, g


def correlation(xs: list[float], ys: list[float]) -> float | None:
    n = len(xs)
    mx, my = sum(xs) / n, sum(ys) / n
    sxx = sum((x - mx) ** 2 for x in xs)
    syy = sum((y - my) ** 2 for y in ys)
    if sxx == 0 or syy == 0:
        return None
    return sum((x - mx) * (y - my) for x, y in zip(xs, ys)) / math.sqrt(sxx * syy)


def run_noise(scores: dict[str, list[float]], cases: list[str]) -> tuple[float | None, float]:
    """Pooled within-case variance of single runs (divisor sum of K-1) and mean K."""
    num = den = 0.0
    for case in cases:
        runs = scores[case]
        if len(runs) >= 2:
            m = sum(runs) / len(runs)
            num += sum((r - m) ** 2 for r in runs)
            den += len(runs) - 1
    mean_k = sum(len(scores[c]) for c in cases) / len(cases)
    return (num / den if den else None), mean_k


def clusters_needed(per_cluster_var: float, delta: float, alpha: float, power: float) -> int | None:
    """Clusters needed to detect delta; z first, then refined with t on G-1 df."""
    if delta <= 0 or per_cluster_var <= 0:
        return None
    z = NormalDist().inv_cdf
    g = math.ceil((z(1 - alpha / 2) + z(power)) ** 2 * per_cluster_var / delta ** 2)
    if g > MAX_PLAN_CASES:
        return None
    g = max(g, 2)
    for _ in range(100):
        df = g - 1
        new = math.ceil((t_quantile(1 - alpha / 2, df) + t_quantile(power, df)) ** 2 * per_cluster_var / delta ** 2)
        new = max(new, 2)
        if new == g:
            break
        g = new
    return g


def analyse(baseline: Path, candidate: Path, alpha: float, power: float,
            target: float | None, plan_runs: int | None, plan_cases: int | None = None) -> dict:
    base, base_scen, base_infra = load_arm(baseline)
    cand, cand_scen, cand_infra = load_arm(candidate)
    for case in set(base_scen) & set(cand_scen):
        if base_scen[case] != cand_scen[case]:
            raise InputError(f"case {case!r} has a different scenario in the two files")
    scenario_of = {**base_scen, **cand_scen}
    paired = sorted(c for c in set(base) & set(cand) if base[c] and cand[c])
    unpaired = sorted((set(base) | set(cand)) - set(paired))
    report: dict = {
        "method": "paired difference of per-case means; SE clustered on "
                  + ("scenario" if scenario_of else "case") + " with G/(G-1); t interval on G-1 df",
        "alpha": alpha, "power": power,
        "cases_paired": len(paired), "cases_unpaired": unpaired,
        "infra_error_rows": {"baseline": base_infra, "candidate": cand_infra},
    }
    if len(paired) < 2:
        report["incomplete"] = "fewer than two cases scored in both files"
        return report
    xb = {c: sum(base[c]) / len(base[c]) for c in paired}
    xc = {c: sum(cand[c]) / len(cand[c]) for c in paired}
    diff = {c: xc[c] - xb[c] for c in paired}
    n = len(paired)
    mean_d = sum(diff.values()) / n
    se, g = clustered_se(diff, scenario_of)
    se_b, _ = clustered_se(xb, scenario_of)
    se_c, _ = clustered_se(xc, scenario_of)
    report.update({
        "clusters": g,
        "baseline": {"mean": sum(xb.values()) / n, "se": se_b},
        "candidate": {"mean": sum(xc.values()) / n, "se": se_c},
        "correlation": correlation([xb[c] for c in paired], [xc[c] for c in paired]),
        "difference": mean_d, "se": se,
    })
    if g < 2:
        report["incomplete"] = "fewer than two scenarios: no interval can be estimated"
        return report
    df = g - 1
    tq = t_quantile(1 - alpha / 2, df)
    low, high = mean_d - tq * se, mean_d + tq * se
    mdd = (tq + t_quantile(power, df)) * se
    report.update({
        "df": df, "interval": [low, high], "minimum_detectable_difference": mdd,
        "verdict": "improved" if low > 0 else "worse" if high < 0 else "within noise",
    })
    if se == 0:
        report["note"] = "every case moved by the same amount; the interval has no width and says nothing about other cases"
    sigma_b, k_b = run_noise(base, paired)
    sigma_c, k_c = run_noise(cand, paired)
    per_case_var = n * se * se          # variance of one case's difference, clustering included; one scenario's is this / cases_per_cluster
    cases_per_cluster = n / g
    report["runs_per_case"] = {"baseline": k_b, "candidate": k_c}
    split_reason = "each version needs at least two runs of some case"
    between = sigma_b_k = sigma_c_k = None
    if sigma_b is not None and sigma_c is not None:
        noise = sigma_b / k_b + sigma_c / k_c
        report["variance"] = {"per_case": per_case_var, "run_noise_baseline": sigma_b,
                              "run_noise_candidate": sigma_c}
        if noise > per_case_var:
            # On a small sample the run-noise estimate can exceed the variance it is part of,
            # so the split cannot be trusted; plan on cases at the runs per case already used.
            split_reason = ("the run-noise estimate exceeds the observed variance on this sample, so the split "
                            "between run noise and case variation is not estimable; plan on cases at the current "
                            "runs per case, or collect more cases first")
            report["variance"]["share_from_run_noise"] = None
            report["variance"]["note"] = split_reason
        else:
            between, sigma_b_k, sigma_c_k = per_case_var - noise, sigma_b, sigma_c
            report["variance"]["between_cases"] = between
            report["variance"]["share_from_run_noise"] = noise / per_case_var if per_case_var > 0 else None

    def var_at(runs: int | None) -> float | None:
        """Per-case variance of the difference at this many runs per case (None: as observed)."""
        if runs is None:
            return per_case_var
        if between is None:
            return None
        return between + sigma_b_k / runs + sigma_c_k / runs

    if target is not None or plan_cases is not None:
        plan: dict = {"assumes": f"{cases_per_cluster:.2f} cases per {'scenario' if scenario_of else 'case'}, "
                                 "as in this sample"}
        for label, runs in (("at_current_runs", None), ("at_planned_runs", plan_runs)):
            if label == "at_planned_runs" and runs is None:
                continue
            v = var_at(runs)
            entry: dict = {"runs_per_case": runs if runs is not None else round((k_b + k_c) / 2, 2)}
            if v is None:
                entry["not_estimable"] = split_reason
                plan[label] = entry
                continue
            if target is not None:
                g_need = clusters_needed(v / cases_per_cluster, target, alpha, power)
                entry["cases_needed"] = None if g_need is None else math.ceil(g_need * cases_per_cluster)
                if scenario_of:
                    entry["scenarios_needed"] = g_need
            if plan_cases is not None:
                g_plan = plan_cases / cases_per_cluster
                if g_plan < 2:
                    entry["detectable_with_planned_cases"] = None
                else:
                    df_plan = g_plan - 1
                    entry["detectable_with_planned_cases"] = (
                        (t_quantile(1 - alpha / 2, df_plan) + t_quantile(power, df_plan))
                        * math.sqrt(v / cases_per_cluster / g_plan))
            plan[label] = entry
        if target is not None:
            plan["target_difference"] = target
            plan["detectable_now"] = mdd <= target
        if plan_cases is not None:
            plan["planned_cases"] = plan_cases
        report["plan"] = plan
    return report


# ---------------------------------------------------------------- output


def pct(value: float) -> str:
    return f"{value * 100:+.1f}" if value is not None and math.isfinite(value) else "n/a"


def plain(value: float) -> str:
    return f"{value * 100:.1f}" if value is not None and math.isfinite(value) else "n/a"


def text_report(r: dict) -> str:
    lines = [f"cases scored in both: {r['cases_paired']}; unpaired: {len(r['cases_unpaired'])}"
             + (f" ({', '.join(r['cases_unpaired'][:20])}{' ...' if len(r['cases_unpaired']) > 20 else ''})"
                if r["cases_unpaired"] else "")]
    infra = r["infra_error_rows"]
    if infra["baseline"] or infra["candidate"]:
        lines.append(f"infra_error rows left out: baseline {infra['baseline']}, candidate {infra['candidate']}")
    if "difference" in r:
        lines.append(f"baseline {plain(r['baseline']['mean'])} (SE {plain(r['baseline']['se'])}); "
                     f"candidate {plain(r['candidate']['mean'])} (SE {plain(r['candidate']['se'])}); "
                     f"points on a 0-100 scale")
        corr = r["correlation"]
        lines.append(f"paired difference {pct(r['difference'])} (SE {plain(r['se'])}); clusters {r['clusters']}; "
                     f"correlation {'n/a' if corr is None else f'{corr:.2f}'}")
    if "interval" in r:
        level = round((1 - r["alpha"]) * 100)
        lines.append(f"{level}% interval {pct(r['interval'][0])} to {pct(r['interval'][1])}; "
                     f"verdict: {r['verdict']}")
        lines.append(f"minimum detectable difference at {round(r['power'] * 100)}% power: {plain(r['minimum_detectable_difference'])} points")
        k = r["runs_per_case"]
        lines.append(f"runs per case: baseline {k['baseline']:.2f}, candidate {k['candidate']:.2f}")
        if "variance" in r:
            share = r["variance"]["share_from_run_noise"]
            lines.append("share of the variance from run-to-run noise: "
                         + (f"{share * 100:.0f}%" if share is not None else f"not estimable ({r['variance']['note']})"))
        if "note" in r:
            lines.append(f"note: {r['note']}")
    if "plan" in r:
        p = r["plan"]
        lines.append(f"planning assumes {p['assumes']}")
        for label in ("at_current_runs", "at_planned_runs"):
            entry = p.get(label)
            if entry is None:
                continue
            head = f"at {entry['runs_per_case']} runs per case"
            if "not_estimable" in entry:
                lines.append(f"{head}: not estimable ({entry['not_estimable']})")
                continue
            if "target_difference" in p:
                need = entry.get("cases_needed")
                lines.append(f"{head}, to detect {plain(p['target_difference'])} points: "
                             + (f"about {need} cases" if need is not None else "not plannable from this variance")
                             + (f" ({entry['scenarios_needed']} scenarios)" if entry.get("scenarios_needed") else ""))
            if "planned_cases" in p:
                mdd = entry.get("detectable_with_planned_cases")
                lines.append(f"{head}, {p['planned_cases']} cases could detect: "
                             + (f"{plain(mdd)} points" if mdd is not None else "nothing (fewer than two clusters)"))
        if "target_difference" in p:
            lines.append(f"this sample {'can' if p['detectable_now'] else 'cannot'} detect "
                         f"{plain(p['target_difference'])} points")
    if "incomplete" in r:
        lines.append(f"INCOMPLETE: {r['incomplete']}")
    elif r["cases_unpaired"]:
        lines.append("INCOMPLETE: some cases have scores in one file only")
    return "\n".join(lines)


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--baseline", type=Path, required=True, help="trial record of the baseline version (CSV or JSONL)")
    parser.add_argument("--candidate", type=Path, required=True, help="trial record of the candidate version (CSV or JSONL)")
    parser.add_argument("--alpha", type=float, default=0.05, help="two-sided significance level (default 0.05)")
    parser.add_argument("--power", type=float, default=0.8, help="power for the detectable difference (default 0.8)")
    parser.add_argument("--target-difference", type=float,
                        help="smallest difference worth acting on, on the score's scale (0.05 is five points)")
    parser.add_argument("--plan-runs", type=int,
                        help="with --target-difference or --plan-cases: also plan for this many runs per case")
    parser.add_argument("--plan-cases", type=int,
                        help="report the difference a set of this many cases could detect (a holdout the budget buys)")
    parser.add_argument("--require", choices=("improved", "not-worse"), help="exit 1 unless this holds")
    parser.add_argument("--margin", type=float, help="with --require not-worse: the largest loss allowed")
    parser.add_argument("--json", action="store_true", help="print a JSON report")
    args = parser.parse_args(argv)
    if not 0 < args.alpha < 1 or not 0.5 <= args.power < 1:
        parser.error("--alpha must be in (0, 1) and --power in [0.5, 1)")
    if args.target_difference is not None and args.target_difference <= 0:
        parser.error("--target-difference must be positive")
    if args.plan_runs is not None and (args.plan_runs < 1 or (args.target_difference is None
                                                             and args.plan_cases is None)):
        parser.error("--plan-runs needs a positive count and --target-difference or --plan-cases")
    if args.plan_cases is not None and args.plan_cases < 2:
        parser.error("--plan-cases must be at least 2")
    if args.require == "not-worse" and (args.margin is None or args.margin < 0):
        parser.error("--require not-worse needs --margin of zero or more")
    if args.margin is not None and args.require != "not-worse":
        parser.error("--margin is used only with --require not-worse")
    try:
        report = analyse(args.baseline, args.candidate, args.alpha, args.power,
                         args.target_difference, args.plan_runs, args.plan_cases)
    except InputError as exc:
        print(f"paired_difference.py: {exc}", file=sys.stderr)
        return BAD_INPUT
    if args.require and "interval" in report:
        low = report["interval"][0]
        met = low > 0 if args.require == "improved" else low > -args.margin
        report["require"] = {"rule": args.require, "margin": args.margin, "met": met}
    print(json.dumps(report, indent=2) if args.json else text_report(report))
    if "incomplete" in report or report["cases_unpaired"]:
        return INCOMPLETE
    if args.require and not report["require"]["met"]:
        return NOT_MET
    return OK


if __name__ == "__main__":
    sys.exit(main())
