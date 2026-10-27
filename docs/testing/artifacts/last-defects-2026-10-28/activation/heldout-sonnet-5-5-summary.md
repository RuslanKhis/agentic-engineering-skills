Activation run: backend claude-cli, model claude-sonnet-5-5, 78 cases x 2 repeat(s), split heldout
catalogue 1156bd511cea6af7  corpus 1b1176c4e0116a18

| Run | PASS | PARTIAL | FAIL | ERROR |
| --- | --- | --- | --- | --- |
| repeat 1 | 77 | 1 | 0 | 0 |
| repeat 2 | 78 | 0 | 0 | 0 |
| all | 155 | 1 | 0 | 0 |

| Split | PASS | PARTIAL | FAIL | ERROR |
| --- | --- | --- | --- | --- |
| heldout | 155 | 1 | 0 | 0 |

Cases not passing in every repeat:
- model-output-heldout-4 [adk-model-and-output-contracts, near-miss, heldout] PARTIAL PASS: primary adk-workflow-design; supporting adk-model-and-output-contracts. Lost session-state handoff of the parsed result across turns on Agent Engine is a session-state/output_key runtime contract issue, with the output parsing side as secondary.
