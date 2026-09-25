I recommend **one ADK application on Cloud Run**, using your existing React app, login, PostgreSQL and ticketing API. Gemini handles language; backend code enforces customer access and submits the exact confirmed escalation.

The [first design](design.md) includes service choices, request flows, access and confirmation contracts, costs, failure recovery and an implementation slice. It remains **draft**, with assumptions marked explicitly.

The main unresolved risk is ticket creation: searching by request reference does not establish safe retries. The design makes one create attempt per operation and preserves uncertain outcomes for reconciliation until the provider contract is verified.

The cost example suggests a modest pilot could fit an **incremental USD $100/month** budget. Currency, existing costs and monthly volume remain open. The five-second target needs cold/warm browser measurements. No code, cloud changes or paid tests were run.
