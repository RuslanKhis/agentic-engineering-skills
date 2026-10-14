"""Package before/after outputs per scenario as blind A/B folders for grading."""
import json, random, shutil, subprocess, sys
from pathlib import Path
R = Path(sys.argv[1]); out = R / "grade"; shutil.rmtree(out, ignore_errors=True)
rng = random.Random(20261015); mapping = {}
for j in ["K1", "K2"]:
    conds = ["before", "after"]; rng.shuffle(conds)
    mapping[j] = {"A": conds[0], "B": conds[1]}
    for label, cond in zip("AB", conds):
        src, dst = R / cond / j, out / j / label
        dst.mkdir(parents=True)
        for f in src.rglob("*"):
            rel = f.relative_to(src)
            if f.is_file() and not rel.parts[0].startswith(".") and "__pycache__" not in rel.parts:
                (dst / rel).parent.mkdir(parents=True, exist_ok=True); shutil.copy2(f, dst / rel)
        msgs = []
        for name in (f"{cond}-{j}.json", f"{cond}-{j}-turn2.json"):
            p = R / name
            if p.exists():
                msgs.append(json.loads(p.read_text()).get("result", ""))
        (dst / "final-message.md").write_text("\n\n---- next turn ----\n\n".join(msgs))
(R / "blind_mapping.json").write_text(json.dumps(mapping, indent=1))
print("packaged", mapping.keys())
