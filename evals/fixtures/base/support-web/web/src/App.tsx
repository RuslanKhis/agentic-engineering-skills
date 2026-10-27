import { ChatPanel } from "./chat/ChatPanel";

export default function App() {
  return (
    <main className="app-shell">
      <header className="app-header">
        <h1>Harbour Outfitters support</h1>
      </header>
      <ChatPanel />
    </main>
  );
}
