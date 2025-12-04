import React, { useState } from "react";

export default function ChatInput({ onSend }) {
  const [text, setText] = useState("");
  const handleSend = () => {
    if (!text.trim()) return;
    onSend(text.trim());
    setText("");
  };
  const onKeyDown = (e) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };
  return (
    <div className="p-4 border-t flex items-center gap-3">
      <textarea
        value={text}
        onChange={(e) => setText(e.target.value)}
        onKeyDown={onKeyDown}
        placeholder="Type your message... (Press Enter to send)"
        className="flex-1 rounded-md p-2 border resize-none h-12"
      />
      <button onClick={handleSend} className="bg-sky-600 text-white px-4 py-2 rounded-md">Send</button>
    </div>
  );
}