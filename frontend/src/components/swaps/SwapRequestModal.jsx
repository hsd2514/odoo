import React, { useState, useEffect } from "react";
import axios from "axios";

/**
 * SwapRequestModal.jsx
 * DaisyUI modal for requesting a swap with correct fields (receiver, skills, time).
 * Usage: <SwapRequestModal open={open} onClose={...} receiver={user} />
 */
export default function SwapRequestModal({ open, onClose, receiver, currentUser, onSuccess }) {
  const [skills, setSkills] = useState([]);
  const [form, setForm] = useState({ skill_offered: "", skill_requested: "", scheduled_time: "" });
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [success, setSuccess] = useState("");

  useEffect(() => {
    if (open) {
      axios.get("/skills/").then(res => setSkills(res.data));
    }
  }, [open]);

  function handleChange(e) {
    const { name, value } = e.target;
    setForm(f => ({ ...f, [name]: value }));
  }

  function handleSubmit(e) {
    e.preventDefault();
    setLoading(true);
    setError("");
    setSuccess("");
    axios.post("/swaps/", {
      receiver_id: receiver.id,
      skill_offered: form.skill_offered,
      skill_requested: form.skill_requested,
      scheduled_time: form.scheduled_time || null
    })
      .then(() => {
        setSuccess("Swap request sent!");
        setForm({ skill_offered: "", skill_requested: "", scheduled_time: "" });
        setLoading(false);
        if (onSuccess) onSuccess();
      })
      .catch(() => {
        setError("Failed to send request");
        setLoading(false);
      });
  }

  if (!open) return null;
  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-base-200 bg-opacity-80 px-2">
      <form className="card bg-base-100 shadow-2xl max-w-md w-full relative p-6 border border-primary/20" onSubmit={handleSubmit}>
        <button type="button" className="btn btn-ghost btn-circle absolute right-3 top-3 text-lg" onClick={onClose} aria-label="Close">✕</button>
        <h2 className="card-title text-center mb-4 text-primary">Request a Swap</h2>
        <div className="flex flex-col items-center mb-4">
          <div className="avatar mb-2">
            <div className="w-16 rounded-full ring ring-primary ring-offset-base-100 ring-offset-2">
              <img src={receiver?.photo_url || 'https://placehold.co/64x64'} alt="Profile" />
            </div>
          </div>
          <div className="font-semibold text-lg">{receiver?.name}</div>
          <div className="text-sm text-gray-500">{receiver?.location}</div>
        </div>
        <div className="form-control mb-3">
          <label className="label font-semibold">Offered Skill</label>
          <select name="skill_offered" className="select select-bordered" value={form.skill_offered} onChange={handleChange} required>
            <option value="">Select skill</option>
            {skills.map(s => <option key={s.id} value={s.id}>{s.name}</option>)}
          </select>
        </div>
        <div className="form-control mb-3">
          <label className="label font-semibold">Wanted Skill</label>
          <select name="skill_requested" className="select select-bordered" value={form.skill_requested} onChange={handleChange} required>
            <option value="">Select skill</option>
            {skills.map(s => <option key={s.id} value={s.id}>{s.name}</option>)}
          </select>
        </div>
        <div className="form-control mb-3">
          <label className="label font-semibold">Scheduled Time <span className="text-xs text-gray-400">(optional)</span></label>
          <input type="datetime-local" name="scheduled_time" className="input input-bordered" value={form.scheduled_time} onChange={handleChange} />
        </div>
        {error && <div className="alert alert-error mb-2">{error}</div>}
        {success && <div className="alert alert-success mb-2">{success}</div>}
        <button className="btn btn-primary btn-block mt-2" type="submit" disabled={loading}>{loading ? "Sending..." : "Send Request"}</button>
      </form>
    </div>
  );
}
