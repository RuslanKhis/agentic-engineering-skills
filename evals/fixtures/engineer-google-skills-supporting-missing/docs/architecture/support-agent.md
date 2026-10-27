# Design: support agent on Cloud Run

Status: accepted 2026-10-16

## Requirements

- R1 Customers reach the assistant only through the shop's existing HTTPS load balancer
  (`harbour-web-lb`, global external Application Load Balancer, Cloud Armor policy
  `harbour-edge`), never on a public `run.app` URL.
- R2 The service holds no long-lived keys; payments and mail credentials come from Secret Manager.

## Contracts

| ID | From | Invariant | Scope | Authority | Enforcement (and recheck at the effect) | Failure outcome | Evidence |
| --- | --- | --- | --- | --- | --- | --- | --- |
| C1 | R1 | the service answers only traffic that came through the load balancer | service | Cloud Run ingress | ingress setting on the service | 403/404 from Cloud Run | planned: G04 readback |
| C2 | R2 | the runtime identity holds only the roles the agent needs | service | IAM | dedicated service account, no default compute SA | permission denied | planned: G04 readback |
| C3 | R2 | no secret value in the image, env file or repository | service | Secret Manager | secret references on the service | start-up fails | planned: G04 |

## Environment

- Projects: `harbour-support-dev` (dev), `harbour-support-prod` (later).
- Region: europe-west2.
- Load balancer: in project `harbour-web-prod`, managed by the web platform team; a serverless NEG
  for the service is added by them on request.
