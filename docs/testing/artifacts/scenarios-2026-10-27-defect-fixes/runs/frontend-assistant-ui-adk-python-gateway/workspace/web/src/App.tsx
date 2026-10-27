import { AdkProvider } from "./adk/AdkProvider";
import { Thread } from "./adk/Thread";

export default function App() {
  return (
    <main className="app-shell">
      <header className="app-header">
        <h1>Harbour Outfitters support</h1>
      </header>
      <AdkProvider>
        <Thread />
      </AdkProvider>
    </main>
  );
}
