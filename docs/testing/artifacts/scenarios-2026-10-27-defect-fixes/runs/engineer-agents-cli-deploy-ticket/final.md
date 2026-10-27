I filled in the G06 Evidence section from a read-only review, and nothing has been run or deployed. This session had no shell, so I couldn't run the unit tests, the inspect helper, Terraform or the CLI. I read the manifest, the Terraform, `deployment_metadata.json`, the agent files and the Agent Runtime reference by hand. The only file I changed is `docs/tickets/G06.md`. The ticket status stays `ready`.

**Findings:**
1. **Dev engine would be overwritten.** `deployment_metadata.json` still points at the dev engine. Running `agents-cli deploy` as things stand would overwrite that engine and leave the pilot untouched. The order has to be Terraform apply first, then repoint the file at the new pilot engine ID, then deploy with `--update-only`.
2. **A1 (Terraform owns the engine) holds on paper.** `main.tf` declares the engine in `claims-helper-pilot` and ignores changes to the code fields. That only works if Terraform creates the engine first.
3. **A2 (own identity, least roles) is partly met.** Agent Identity is set, but Terraform grants no roles. The CLI grants them at deploy time, and its `aiplatform.user` is broader than the documented `expressUser`. Nothing grants `roles/cloudtrace.agent`, so the traces the design expects may not arrive.
4. **A3 (previous version restorable) is blocked.** There is no git repository and no record of a prior pilot version, so no rollback path is shown. Terraform state is also local, because there is no backend block.

**Questions I couldn't ask, and what I assumed:**
- I kept local Terraform state for the pilot rather than a remote bucket.
- I accepted `aiplatform.user` for the pilot and flagged it.
- I left the inference location at the CLI default (`global`) while hosting stays in `europe-west1`. If the pilot has a data-residency need, that needs deciding.
- I left the idle cost as written, since reading it needs the pricing page and there is no network here.

**Left undone:**
- All tests and live checks are `not run` or `blocked`. Please run `python -m unittest discover -s tests -t .` before review.
- Your approval is still needed. The ticket lists the exact commands I propose, with cleanup, for you to approve or amend: `terraform init`, `plan` and `apply`, then the metadata edit, then `agents-cli deploy --update-only --dry-run` and the real deploy, then the readback. I haven't run any of them. The CLI flags need checking against `agents-cli deploy --help`, since the CLI isn't installed here.