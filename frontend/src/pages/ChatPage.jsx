import React, { useEffect, useRef, useState, useContext } from "react";
import { AuthContext } from "../context/AuthContext";

// DaisyUI + Tailwind chat UI
const ChatPage = () => {
  const { user, token } = useContext(AuthContext);
  const [otherUserId, setOtherUserId] = useState("");
  const [connected, setConnected] = useState(false);
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState("");
  const wsRef = useRef(null);
  const chatBottomRef = useRef(null);

  // Scroll to bottom on new message
  useEffect(() => {
    if (chatBottomRef.current) chatBottomRef.current.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  const connect = () => {
    if (!otherUserId || !token) return;
    const ws = new WebSocket(
      `${import.meta.env.VITE_API_WS || "ws://localhost:8000"}/ws/chat/${otherUserId}?token=${token}`
    );
    ws.onopen = () => setConnected(true);
    ws.onclose = () => setConnected(false);
    ws.onmessage = (e) => {
      const data = JSON.parse(e.data);
      if (data.type === "history") setMessages(data.messages);
      if (data.type === "message") setMessages((msgs) => [...msgs, data]);
    };
    wsRef.current = ws;
  };

  const send = () => {
    if (wsRef.current && input.trim()) {
      wsRef.current.send(JSON.stringify({ message: input }));
      setInput("");
    }
  };

  return (
    <div className="flex flex-col items-center justify-center min-h-screen bg-base-200">
      <div className="card w-full max-w-md bg-base-100 shadow-xl">
        <div className="card-body">
          <h2 className="card-title">Chat</h2>
          {!connected ? (
            <div className="flex flex-col gap-2">
              <input
                className="input input-bordered"
                placeholder="Enter user ID to chat with"
                value={otherUserId}
                onChange={(e) => setOtherUserId(e.target.value)}
                type="number"
              />
              <button className="btn btn-primary" onClick={connect} disabled={!otherUserId}>
                Connect
              </button>
            </div>
          ) : (
            <>
              <div className="overflow-y-auto h-64 mb-2 bg-base-200 rounded p-2">
                {messages.map((msg, i) => (
                  <div
                    key={i}
                    className={`chat ${msg.from === user?.id ? "chat-end" : "chat-start"}`}
                  >
                    <div className="chat-header">
                      {msg.from === user?.id ? "You" : `User ${msg.from}`}
                    </div>
                    <div className="chat-bubble">{msg.message}</div>
                  </div>
                ))}
                <div ref={chatBottomRef} />
              </div>
              <div className="flex gap-2">
                <input
                  className="input input-bordered flex-1"
                  placeholder="Type a message..."
                  value={input}
                  onChange={(e) => setInput(e.target.value)}
                  onKeyDown={(e) => e.key === "Enter" && send()}
                />
                <button className="btn btn-secondary" onClick={send} disabled={!input.trim()}>
                  Send
                </button>
              </div>
            </>
          )}
        </div>
      </div>
    </div>
  );
};

export default ChatPage;
