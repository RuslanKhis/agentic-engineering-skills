import { Route, Routes } from "react-router";
import { Chat } from "./Chat";

export function App() {
  return (
    <Routes>
      <Route path="/" element={<Chat />} />
      <Route path="/c/:conversationId" element={<Chat />} />
    </Routes>
  );
}
