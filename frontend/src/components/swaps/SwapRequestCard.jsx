import React from "react";

/**
 * SwapRequestCard.jsx
 * DaisyUI + Tailwind card for a single swap request, with status and accept/reject buttons if actionable.
 * For beginners: Shows swap request details and lets you accept/reject if needed.
 */
export default function SwapRequestCard({ request, onAccept, onReject }) {
  return (
    <div className="card bg-base-100 shadow mb-4">
      <div className="card-body">
        <h3 className="card-title">{request.offered_skill} ⇄ {request.wanted_skill}</h3>
        <p><b>From:</b> {request.from_user_name}</p>
        <p><b>To:</b> {request.to_user_name}</p>
        <p><b>Message:</b> {request.message}</p>
        <p><b>Status:</b> <span className={`badge badge-${request.status === "pending" ? "info" : request.status === "accepted" ? "success" : "error"}`}>{request.status}</span></p>
        {request.status === "pending" && (
          <div className="card-actions mt-2">
            {onAccept && <button className="btn btn-success" onClick={() => onAccept(request.id)}>Accept</button>}
            {onReject && <button className="btn btn-error" onClick={() => onReject(request.id)}>Reject</button>}
          </div>
        )}
      </div>
    </div>
  );
}
