# Implementation plan: support agent on Cloud Run

Status: in progress
Architecture: [docs/architecture/support-agent.md](../architecture/support-agent.md)

## Goals and dependencies

| ID and goal | Phase | Type | Human hours | Depends on | Primary skill | State / blocker |
| --- | --- | --- | --- | --- | --- | --- |
| G01 Order lookups and refunds | 1 | implementation | 3-5 | none | safe-api-tool-calls | done |
| G02 Help-centre search | 1 | implementation | 1-2 | none | adk-memory-architecture | done |
| G03 IAP-verified principal | 1 | implementation | 1-2 | none | adk-fastapi-backend | done |
| [G04 Deploy privately behind the load balancer](../tickets/support-agent/G04.md) | 1 | implementation | 3-4.5 | G01-G03 | deploy-adk-on-google-cloud | ready; W1 for the NEG |
| G05 Pilot review | 1 | presentation | 2-3 | G04 | adk-presenter | planned |

## Waits

| ID | What | Owner | Days |
| --- | --- | --- | --- |
| W1 | Serverless NEG and URL-map route on `harbour-web-lb` | web platform team | 2-5 |

## Execution scope

Authorised now: local image build. Not yet authorised: any change in harbour-support-dev or
harbour-web-prod (deploy, IAM, secrets); each needs Priya's approval of the exact commands.
