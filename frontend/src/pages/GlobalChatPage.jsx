import React, { useEffect, useRef, useState, useContext } from "react";
import { AuthContext } from "../context/AuthContext";

// DaisyUI + Tailwind global chat UI
const GlobalChatPage = () => {
  const { user, token } = useContext(AuthContext);
  const [connected, setConnected] = useState(false);
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState("");
  const wsRef = useRef(null);
  const chatBottomRef = useRef(null);
  const [wsError, setWsError] = useState(null);

  useEffect(() => {
    if (chatBottomRef.current) chatBottomRef.current.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  useEffect(() => {
    if (!token) return;
    setWsError(null);
    const wsUrl = `${import.meta.env.VITE_API_WS || "ws://localhost:8000"}/ws/global-chat?token=${token}`;
    console.log("Connecting to WebSocket:", wsUrl);
    const ws = new WebSocket(wsUrl);
    let timeout = setTimeout(() => {
      if (!connected) {
        setWsError(`WebSocket did not connect after 5 seconds. Is your backend running at ${wsUrl}?`);
        ws.close();
      }
    }, 5000);
    ws.onopen = () => {
      setConnected(true);
      clearTimeout(timeout);
      console.log("WebSocket connected");
    };
    ws.onclose = (e) => {
      setConnected(false);
      setWsError(`WebSocket connection closed. Code: ${e.code}. Reason: ${e.reason || "No reason"}. URL: ${wsUrl}`);
      clearTimeout(timeout);
      console.error("WebSocket closed", e);
    };
    ws.onerror = (e) => {
      setConnected(false);
      setWsError(`WebSocket error. URL: ${wsUrl}. Please check your backend and network.`);
      clearTimeout(timeout);
      console.error("WebSocket error", e);
    };
    ws.onmessage = (e) => {
      const data = JSON.parse(e.data);
      if (data.type === "history") setMessages(data.messages);
      if (data.type === "message") setMessages((msgs) => [...msgs, data]);
    };
    wsRef.current = ws;
    return () => {
      clearTimeout(timeout);
      ws.close();
    };
  }, [token]);

  const send = () => {
    if (wsRef.current && input.trim() && connected) {
      wsRef.current.send(JSON.stringify({ message: input }));
      setInput("");
    }
  };

  return (
    <div className="flex flex-col items-center justify-center min-h-screen bg-base-200">
      <div className="card w-full max-w-md bg-base-100 shadow-xl">
        <div className="card-body">
          <h2 className="card-title">Global Chat Room</h2>
          {wsError && <div className="alert alert-error mb-2">{wsError}</div>}
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
              placeholder={connected ? "Type a message..." : wsError ? "Connection error" : "Connecting..."}
              value={input}
              onChange={(e) => setInput(e.target.value)}
              onKeyDown={(e) => e.key === "Enter" && send()}
              disabled={!connected}
            />
            <button className="btn btn-secondary" onClick={send} disabled={!input.trim() || !connected}>
              Send
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};

export default GlobalChatPage;
