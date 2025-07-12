import React, { useState } from "react";

/**
 * SwapRequestCard.jsx
 * DaisyUI + Tailwind card for a single swap request, with status and accept/reject buttons if actionable.
 * For beginners: Shows swap request details and lets you accept/reject if needed.
 */
export default function SwapRequestCard({ request, onAccept, onReject, onFeedback }) {
  const [showFeedback, setShowFeedback] = useState(false);
  const [rating, setRating] = useState(0);
  const [feedback, setFeedback] = useState("");

  function handleSubmit(e) {
    e.preventDefault();
    onFeedback(request.id, rating, feedback);
    setShowFeedback(false);
    setRating(0);
    setFeedback("");
  }

  return (
    <div className="card bg-base-100 shadow mb-4">
      <div className="card-body">
        <h3 className="card-title">{request.skill_offered_name} ⇄ {request.skill_requested_name}</h3>
        <p><b>From:</b> {request.sender_name}</p>
        <p><b>To:</b> {request.receiver_name}</p>
        <p><b>Message:</b> {request.message || <span className="text-gray-400">(none)</span>}</p>
        <p><b>Status:</b> <span className={`badge badge-${request.status === "pending" ? "info" : request.status === "accepted" ? "success" : "error"}`}>{request.status}</span></p>
        {request.status === "pending" && (
          <div className="card-actions mt-2">
            {onAccept && <button className="btn btn-success" onClick={() => onAccept(request.id)}>Accept</button>}
            {onReject && <button className="btn btn-error" onClick={() => onReject(request.id)}>Reject</button>}
          </div>
        )}
        {request.status === "accepted" && (
          <div className="mt-2">
            <button className="btn btn-outline btn-sm" onClick={() => setShowFeedback(f => !f)}>
              {showFeedback ? "Hide Feedback" : "Leave Feedback"}
            </button>
            {showFeedback && (
              <form className="mt-2 flex flex-col gap-2" onSubmit={handleSubmit}>
                <label className="font-semibold">Rating:</label>
                <select className="select select-bordered" value={rating} onChange={e => setRating(Number(e.target.value))} required>
                  <option value={0}>Select rating</option>
                  {[1,2,3,4,5].map(r => <option key={r} value={r}>{r} Star{r>1?"s":""}</option>)}
                </select>
                <label className="font-semibold">Feedback:</label>
                <textarea className="textarea textarea-bordered" value={feedback} onChange={e => setFeedback(e.target.value)} placeholder="Write feedback..." />
                <button className="btn btn-primary btn-sm mt-2" type="submit">Submit</button>
              </form>
            )}
          </div>
        )}
        {request.rating && (
          <div className="mt-2">
            <span className="badge badge-success">Rated: {request.rating} ⭐</span>
            <div className="text-sm text-gray-500">{request.feedback}</div>
          </div>
        )}
      </div>
    </div>
  );
}
