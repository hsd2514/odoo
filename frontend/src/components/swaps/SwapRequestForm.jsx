import React, { useState } from "react";
import axios from "axios";

/**
 * SwapRequestForm.jsx
 * DaisyUI + Tailwind form to request a swap: offered skill, wanted skill, message, submit.
 * For beginners: This form lets you request a skill swap from another user.
 */
export default function SwapRequestForm({ onSuccess }) {
  const [form, setForm] = useState({ offered_skill: "", wanted_skill: "", message: "" });
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [success, setSuccess] = useState("");

  function handleChange(e) {
    const { name, value } = e.target;
    setForm(f => ({ ...f, [name]: value }));
  }

  function handleSubmit(e) {
    e.preventDefault();
    setLoading(true);
    setError("");
    setSuccess("");
    axios.post("/swaps/requests", form)
      .then(() => {
        setSuccess("Swap request sent!");
        setForm({ offered_skill: "", wanted_skill: "", message: "" });
        setLoading(false);
        if (onSuccess) onSuccess();
      })
      .catch(() => {
        setError("Failed to send request");
        setLoading(false);
      });
  }

  return (
    <form className="card bg-base-100 shadow p-4 max-w-md mx-auto" onSubmit={handleSubmit}>
      <h2 className="card-title mb-2">Request a Swap</h2>
      <div className="form-control mb-2">
        <label className="label">Offered Skill</label>
        <input name="offered_skill" className="input input-bordered" value={form.offered_skill} onChange={handleChange} required />
      </div>
      <div className="form-control mb-2">
        <label className="label">Wanted Skill</label>
        <input name="wanted_skill" className="input input-bordered" value={form.wanted_skill} onChange={handleChange} required />
      </div>
      <div className="form-control mb-2">
        <label className="label">Message</label>
        <textarea name="message" className="textarea textarea-bordered" value={form.message} onChange={handleChange} required />
      </div>
      {error && <div className="alert alert-error mb-2">{error}</div>}
      {success && <div className="alert alert-success mb-2">{success}</div>}
      <button className="btn btn-primary w-full" type="submit" disabled={loading}>{loading ? "Sending..." : "Send Request"}</button>
    </form>
  );
}
