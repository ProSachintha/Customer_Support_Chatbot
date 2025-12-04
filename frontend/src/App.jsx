import React, { useState, useEffect, useRef } from "react";
import ChatWindow from "./components/ChatWindow";
import ChatInput from "./components/ChatInput";
import axios from "axios";

export default function App() {
  const [messages, setMessages] = useState([
    { id: 0, from: "bot", text: "Hello! I am your customer support assistant. Ask me about orders, returns, delivery, or products." }
  ]);

  const sendMessage = async (text) => {
    if (!text) return;
    const userMsg = { id: Date.now(), from: "user", text };
    setMessages((m) => [...m, userMsg]);
    try {
      const res = await axios.post("http://localhost:5000/chat", { message: text });
      const botMsg = { id: Date.now()+1, from: "bot", text: res.data.reply };
      setMessages((m) => [...m, botMsg]);
    } catch (err) {
      const botMsg = { id: Date.now()+1, from: "bot", text: "Sorry, the server is unreachable. Make sure the backend is running." };
      setMessages((m) => [...m, botMsg]);
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-slate-100 p-4">
      <div className="w-full max-w-2xl bg-white rounded-2xl shadow-lg flex flex-col" style={{height: "80vh"}}>
        <ChatWindow messages={messages} />
        <ChatInput onSend={sendMessage} />
      </div>
    </div>
  );
}