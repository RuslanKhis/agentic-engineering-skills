# Platform standard: agent evaluations (platform team, 2026-10-15)

All agent teams run their nightly agent evaluations with Promptfoo so results
land in one place. Pin the Promptfoo version in `package.json`. Each team owns
its provider wrapper and assertions. Teams decide how their job reads the
result; the platform only collects the JSON output.
