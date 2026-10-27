Activation run: backend claude-cli, model claude-haiku-5-5, 78 cases x 1 repeat(s), split heldout
catalogue 74e4ed4293f09ed1  corpus df13231d2053304f

| Run | PASS | PARTIAL | FAIL | ERROR |
| --- | --- | --- | --- | --- |
| repeat 1 | 77 | 1 | 0 | 0 |
| all | 77 | 1 | 0 | 0 |

| Split | PASS | PARTIAL | FAIL | ERROR |
| --- | --- | --- | --- | --- |
| heldout | 77 | 1 | 0 | 0 |

Cases not passing in every repeat:
- optimise-heldout-3 [optimise-adk-on-google-cloud, near-miss, heldout] PARTIAL: primary deploy-adk-on-google-cloud; supporting optimise-adk-on-google-cloud. The missing aiplatform.user role for the service account and the RefreshError on Cloud Run are deployment identity issues, with the slowdown and 503s after the first request possibly tied to concurrency and process shape.
