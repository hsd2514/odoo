import React, { useState } from "react";

/**
 * InviteCard.jsx
 * DaisyUI card for displaying a single invite with accept/decline actions and feedback/rating.
 * Props: invite (object), onAccept (function), onDecline (function), onFeedback (function)
 */
/**
 * InviteCard.jsx
 * DaisyUI card for displaying a single invite with accept/decline actions and feedback/rating.
 * Props: invite (object), direction ("incoming" | "outgoing"), onAccept (function), onDecline (function), onFeedback (function)
 */
export default function InviteCard({ invite, direction = "incoming", currentUserId, onAccept, onDecline, onFeedback }) {
  const [showFeedback, setShowFeedback] = useState(false);
  const [rating, setRating] = useState(0);
  const [feedback, setFeedback] = useState("");

  function handleSubmit(e) {
    e.preventDefault();
    if (onFeedback) onFeedback(invite.id, rating, feedback);
    setShowFeedback(false);
    setRating(0);
    setFeedback("");
  }

  return (
    <div className="card bg-base-100 shadow p-4 flex flex-col gap-2">
      <div className="font-semibold">
        {direction === "incoming"
          ? `From: ${invite.sender_name || invite.sender_id}`
          : `To: ${invite.receiver_name || invite.receiver_id}`}
      </div>
      <div>
        Skill: {invite.skill_name
          ? invite.skill_name
          : invite.skill_id
            ? `Skill #${invite.skill_id}`
            : "(unknown)"}
      </div>
      <div>Status: <span className="badge badge-info">{invite.status}</span></div>
      <div className="text-sm text-gray-500">{invite.message}</div>
      <div className="text-xs text-gray-400 mt-1">{invite.created_at ? new Date(invite.created_at).toLocaleString() : ""}</div>
      {invite.status === "pending" && (
        <div className="flex gap-2 mt-2">
          <button className="btn btn-success btn-sm" onClick={() => onAccept(invite.id)}>Accept</button>
          <button className="btn btn-error btn-sm" onClick={() => onDecline(invite.id)}>Decline</button>
        </div>
      )}
      {invite.status === "accepted" && currentUserId === invite.sender_id && (
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
      {invite.rating && (
        <div className="mt-2">
          <span className="badge badge-success">Rated: {invite.rating} ⭐</span>
          <div className="text-sm text-gray-500">{invite.feedback}</div>
        </div>
      )}
    </div>
  );
}
