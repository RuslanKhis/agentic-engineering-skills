import { CopilotKit } from "@copilotkit/react-core";
import { CopilotChat } from "@copilotkit/react-ui";
import "@copilotkit/react-ui/styles.css";
import { RefundApproval } from "./chat/RefundApproval";

export default function App() {
  return (
    <main className="app-shell">
      <header className="app-header">
        <h1>Harbour Outfitters support</h1>
      </header>
      <CopilotKit runtimeUrl="/api/copilotkit" agent="support">
        <RefundApproval />
        <CopilotChat labels={{ initial: "Ask about an order, delivery or refund" }} />
      </CopilotKit>
    </main>
  );
}
