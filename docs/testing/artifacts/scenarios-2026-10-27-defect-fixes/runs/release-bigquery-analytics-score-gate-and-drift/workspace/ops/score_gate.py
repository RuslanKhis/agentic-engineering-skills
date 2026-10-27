"""Nightly production score gate around Google's `bq-agent-sdk evaluate`.

Exit codes (the same for `run` and `check`):
  0  pass     every configured check passed
  1  fail     at least one check failed: the release is blocked
  2  not run  the score could not be produced (BigQuery or auth down, SDK
              missing, timeout, bad config, threshold unset, record missing
              or stale): the release is blocked, never treated as a pass

Standard library only; the SDK is run as a subprocess and is not imported.
"""
import argparse
import json
import os
import re
import subprocess
import sys
import tempfile
import time
from datetime import datetime, timezone

PASS, FAIL, NOT_RUN = 0, 1, 2
STATUS = {PASS: "pass", FAIL: "fail", NOT_RUN: "not_run"}


def load_config(path):
    with open(path, encoding="utf-8") as fh:
        cfg = json.load(fh)
    for key in ("project_id", "dataset_id", "checks"):
        if not cfg.get(key):
            raise ValueError(f"config key {key!r} is missing or empty")
    return cfg


def sanitize(text, limit=300):
    """Make SDK output safe to print in CI logs (no control chars, no workflow commands)."""
    text = re.sub(r"[\x00-\x08\x0b-\x1f\x7f]", "?", text or "")
    text = text.replace("::", ": :")
    return text[-limit:]


def build_command(cfg, check):
    cmd = [
        cfg.get("sdk_command", "bq-agent-sdk"),
        "--project-id", cfg["project_id"],
        "--dataset-id", cfg["dataset_id"],
        "--table-id", cfg.get("table_id", "agent_events"),
        "--format", "json",
        "evaluate",
        "--evaluator", check["evaluator"],
        "--threshold", str(check["threshold"]),
        "--last", cfg.get("window", "24h"),
        "--exit-code",
    ]
    if cfg.get("agent_id"):
        cmd += ["--agent-id", cfg["agent_id"]]
    if check.get("criterion"):
        cmd += ["--criterion", check["criterion"]]
    return cmd


def run_check(cfg, check, runner, sleep, log):
    """Return (code, note). Anything other than the SDK's own 0 or 1 is NOT_RUN."""
    if check.get("threshold") is None:
        return NOT_RUN, "threshold not set"
    attempts = 1 + int(cfg.get("retries", 1))
    code, note = NOT_RUN, "not attempted"
    for attempt in range(attempts):
        try:
            proc = runner(build_command(cfg, check), timeout=cfg.get("timeout_seconds", 900))
        except FileNotFoundError:
            return NOT_RUN, "bq-agent-sdk not installed"
        except subprocess.TimeoutExpired:
            code, note = NOT_RUN, "timeout"
        else:
            if proc.returncode in (PASS, FAIL):
                return proc.returncode, f"sdk exit {proc.returncode}"
            code, note = NOT_RUN, f"sdk exit {proc.returncode}"
            log(sanitize(proc.stderr or proc.stdout))
        if attempt + 1 < attempts:
            sleep(30 * (attempt + 1))
    return code, note


def aggregate(codes):
    if FAIL in codes:
        return FAIL
    return PASS if codes and all(c == PASS for c in codes) else NOT_RUN


def write_record(path, record):
    directory = os.path.dirname(os.path.abspath(path))
    os.makedirs(directory, exist_ok=True)
    fd, tmp = tempfile.mkstemp(dir=directory)
    with os.fdopen(fd, "w", encoding="utf-8") as fh:
        json.dump(record, fh, indent=2)
    os.replace(tmp, path)


def run(cfg, record_path, runner=None, sleep=time.sleep, now=None, log=print):
    runner = runner or (lambda cmd, timeout: subprocess.run(
        cmd, capture_output=True, text=True, timeout=timeout, check=False))
    now = now or datetime.now(timezone.utc)
    results = []
    for check in cfg["checks"]:
        code, note = run_check(cfg, check, runner, sleep, log)
        results.append({"evaluator": check["evaluator"], "threshold": check.get("threshold"),
                        "status": STATUS[code], "note": note})
        log(f"{check['evaluator']}: {STATUS[code]} ({note})")
    final = aggregate([{v: k for k, v in STATUS.items()}[r["status"]] for r in results])
    write_record(record_path, {"schema": 1, "status": STATUS[final], "window": cfg.get("window", "24h"),
                               "evaluated_at": now.isoformat(), "checks": results})
    return final


def check_record(record_path, max_age_hours, now=None, log=print):
    """Release-side check: pass only on a fresh, passing record."""
    now = now or datetime.now(timezone.utc)
    try:
        with open(record_path, encoding="utf-8") as fh:
            rec = json.load(fh)
        age = now - datetime.fromisoformat(rec["evaluated_at"])
        status = rec["status"]
    except (OSError, ValueError, KeyError, TypeError) as exc:
        log(f"no usable score record: {type(exc).__name__}")
        return NOT_RUN
    if age.total_seconds() > max_age_hours * 3600:
        log(f"score record is stale ({age.total_seconds() / 3600:.1f} h old): not run")
        return NOT_RUN
    if status == "pass":
        return PASS
    log(f"last nightly score: {status}")
    return FAIL if status == "fail" else NOT_RUN


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    p_run = sub.add_parser("run", help="score the window and write the record")
    p_run.add_argument("--config", default="ops/score_gate.json")
    p_run.add_argument("--record", default="release/score_gate_record.json")
    p_chk = sub.add_parser("check", help="release-side: block unless a fresh passing record exists")
    p_chk.add_argument("--record", default="release/score_gate_record.json")
    p_chk.add_argument("--max-age-hours", type=float, default=30)
    args = ap.parse_args(argv)
    if args.cmd == "check":
        return check_record(args.record, args.max_age_hours)
    try:
        cfg = load_config(args.config)
    except (OSError, ValueError) as exc:
        print(f"bad config: {type(exc).__name__}: {exc}", file=sys.stderr)
        return NOT_RUN
    return run(cfg, args.record)


if __name__ == "__main__":
    sys.exit(main())
