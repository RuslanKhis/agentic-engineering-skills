# helpdesk-agent

Northbridge IT helpdesk agent, created with Agents CLI (`agents-cli create`,
ADK template, Cloud Run target, Cloud SQL sessions). See `.agents-cli-spec.md` for the accepted
specification.

```bash
uv sync
uv run python -m unittest discover -s tests -t .   # offline unit tests
agents-cli eval run                                 # tests/eval (live model, needs approval)
make playground                                     # local adk web
agents-cli deploy                                   # Cloud Run (needs approval)
```

Environment for this repository copy: google-adk and the other dependencies
are not installed, there are no Google Cloud credentials and no network.
