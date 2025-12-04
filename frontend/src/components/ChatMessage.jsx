import React from "react";

export default function ChatMessage({ message }) {
  const isUser = message.from === "user";
  return (
    <div className={`flex ${isUser ? "justify-end" : "justify-start"}`}>
      <div className={`${isUser ? "bg-sky-500 text-white" : "bg-gray-100 text-gray-900"} max-w-[70%] p-3 rounded-lg`}>
        <div className="text-sm whitespace-pre-line">{message.text}</div>
      </div>
    </div>
  );
}