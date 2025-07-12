import React from "react";
import { Link } from "react-router-dom";

// DaisyUI card/button for chat navigation
const ChatNavCard = () => (
  <div className="card bg-base-100 shadow-md mb-4">
    <div className="card-body flex flex-col items-center">
      <h2 className="card-title">Chat with Users</h2>
      <p className="text-center">Start a real-time chat with any user by their ID.</p>
      <Link to="/chat" className="btn btn-primary mt-2">
        Go to Chat
      </Link>
    </div>
  </div>
);

export default ChatNavCard;
