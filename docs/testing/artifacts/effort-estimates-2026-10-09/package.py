"""Package before/after outputs per scenario as blind A/B folders for grading."""
import json, random, shutil, subprocess, sys
from pathlib import Path
R = Path(sys.argv[1]); out = R / "grade"; shutil.rmtree(out, ignore_errors=True)
rng = random.Random(20261010); mapping = {}
for j in ["H1", "H2", "H3", "H4", "H5", "H6"]:
    conds = ["before", "after"]; rng.shuffle(conds)
    mapping[j] = {"A": conds[0], "B": conds[1]}
    for label, cond in zip("AB", conds):
        src, dst = R / cond / j, out / j / label
        dst.mkdir(parents=True)
        for f in src.rglob("*"):
            rel = f.relative_to(src)
            if f.is_file() and rel.parts[0] not in (".claude", ".git") and "__pycache__" not in rel.parts:
                (dst / rel).parent.mkdir(parents=True, exist_ok=True); shutil.copy2(f, dst / rel)
        diff = subprocess.run(["git", "diff"], cwd=src, capture_output=True, text=True).stdout
        (dst / "changes.diff").write_text(diff)
        res = json.loads((R / f"{cond}-{j}.json").read_text())
        (dst / "final-message.md").write_text(res.get("result", ""))
        (dst / "run.json").write_text(json.dumps({k: res.get(k) for k in ("num_turns", "total_cost_usd", "duration_ms", "is_error")}, indent=1))
(R / "blind_mapping.json").write_text(json.dumps(mapping, indent=1))
print("packaged", list(mapping))
