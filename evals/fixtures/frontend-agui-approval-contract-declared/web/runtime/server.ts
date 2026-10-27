// CopilotKit runtime: forwards the chat to the Python AG-UI endpoint.
import { createServer } from "node:http";
import { HttpAgent } from "@ag-ui/client";
import { CopilotRuntime, ExperimentalEmptyAdapter, copilotRuntimeNodeHttpEndpoint } from "@copilotkit/runtime";

const runtime = new CopilotRuntime({
  agents: {
    support: new HttpAgent({ url: process.env.AGENT_URL ?? "http://localhost:8080/api/agent" }),
  },
});

const handler = copilotRuntimeNodeHttpEndpoint({
  endpoint: "/api/copilotkit",
  runtime,
  serviceAdapter: new ExperimentalEmptyAdapter(),
});

createServer(handler).listen(4000);
