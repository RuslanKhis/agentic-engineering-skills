// Runtime wiring. UNVERIFIED against @assistant-ui/react-google-adk 0.0.40: the option names
// (`stream`, `create`, `getCheckpointId`) and the stream callback's argument were taken from the
// package's documentation, not compiled. Reconcile this one file after `npm install`.
// No `cloud` option: it would copy settled messages to Assistant Cloud.
import type { ReactNode } from "react";
import { AssistantRuntimeProvider } from "@assistant-ui/react";
import { useAdkRuntime } from "@assistant-ui/react-google-adk";
import { checkpointAfter, createSession, runTurn } from "./gatewayApi";

interface StreamRequest {
  sessionId: string;
  parts?: unknown[];
  message?: string;
  checkpointId?: string | null;
  // runConfig, stateDelta and messageId are deliberately not forwarded.
}

export function AdkProvider({ children }: { children: ReactNode }) {
  const runtime = useAdkRuntime({
    // The gateway allocates the session, owned by the verified principal.
    create: async () => ({ externalId: await createSession() }),
    stream: (request: StreamRequest, { abortSignal }: { abortSignal?: AbortSignal }) =>
      runTurn(
        {
          sessionId: request.sessionId,
          parts: request.parts ?? (request.message === undefined ? [] : [{ text: request.message }]),
          ...(request.checkpointId ? { checkpointId: request.checkpointId } : {}),
        },
        abortSignal,
      ),
    getCheckpointId: async (_threadId: string, parents: { id: string; role: string }[]) =>
      checkpointAfter(parents),
  });
  return <AssistantRuntimeProvider runtime={runtime}>{children}</AssistantRuntimeProvider>;
}
