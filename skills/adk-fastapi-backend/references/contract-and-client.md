# The public contract and the generated client

Read when adding or changing a route the browser calls, or setting up the
client and its drift check.

- Every route declares its response type (a return annotation or
  `response_model`) and a bounded request model. Unknown fields are
  forbidden on domain inputs; an agent route may ignore a stale client's
  `user_id` instead, but never uses it.
- Operation IDs are stable and readable: pass
  `generate_unique_id_function=lambda route: f"{route.tags[0]}-{route.name}"`
  (tags required on every router), so regenerated client names do not churn.
- Dump the document offline: a script imports the app factory and writes
  `json.dumps(create_app().openapi(), indent=2, sort_keys=True)`. It must run
  with no credentials and no network, which keeps provisioning out of import
  time. Commit `openapi.json`, so a breaking-change check has a reviewable base.
- Generate the browser client with `@hey-api/openapi-ts` pinned exactly
  (0.99.0 was used here; it is pre-1.0 and needs `typescript` installed as a
  peer): `npx openapi-ts -i openapi.json -o src/client`. Commit `src/client/`.
- `make check` dumps, regenerates and runs `git diff --exit-code openapi.json
  frontend/src/client`. Two generations from one dump were identical in
  testing, so any diff is real drift.
- In a deployed build, docs and the schema are not served (SB07); the client
  comes from the committed dump.
- From MVP: `oasdiff breaking main:openapi.json openapi.json --fail-on ERR`
  in CI, and Schemathesis over the non-agent routes
  (`schemathesis.openapi.from_asgi(...)` in Schemathesis 4.x) finding no 5xx.
- Agent streams stay out of the OpenAPI document: the stream contract belongs
  to `adk-frontend-integration`, and the browser validates each event at run
  time.
