import React, { useState, useEffect } from "react";

import axios from "axios";

axios.defaults.baseURL = "http://localhost:8000";

/**
 * UserProfile.jsx
 * DaisyUI + Tailwind user profile page with edit/save/discard, skills, availability, public/private toggle, and profile photo.
 * For beginners: This component fetches the current user's profile, allows editing, and updates the backend.
 */

const AVAILABILITY_OPTIONS = ["Available", "Busy", "Looking for Opportunities"];

export default function UserProfile() {
  const [profile, setProfile] = useState(null);
  const [editMode, setEditMode] = useState(false);
  const [form, setForm] = useState({});
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  // Fetch profile on mount
  useEffect(() => {
    axios.get("/users/me")
      .then(res => {
        setProfile(res.data);
        setForm(res.data);
        setLoading(false);
      })
      .catch(() => {
        setError("Failed to load profile");
        setLoading(false);
      });
  }, []);

  // Handle form changes
  function handleChange(e) {
    const { name, value, type, checked } = e.target;
    setForm(f => ({
      ...f,
      [name]: type === "checkbox" ? checked : value
    }));
  }

  // Save profile
  function handleSave() {
    setLoading(true);
    axios.put("/users/me", form)
      .then(res => {
        setProfile(res.data);
        setEditMode(false);
        setLoading(false);
      })
      .catch(() => {
        setError("Failed to save profile");
        setLoading(false);
      });
  }

  // Discard changes
  function handleDiscard() {
    setForm(profile);
    setEditMode(false);
  }

  // Handle profile photo upload (dummy for hackathon)
  function handlePhotoChange(e) {
    // For hackathon: just update preview, skip backend upload
    const file = e.target.files[0];
    if (file) {
      const reader = new FileReader();
      reader.onload = ev => setForm(f => ({ ...f, photo_url: ev.target.result }));
      reader.readAsDataURL(file);
    }
  }

  if (loading) return <div className="flex justify-center items-center h-64">Loading...</div>;
  if (error) return <div className="alert alert-error">{error}</div>;
  if (!profile) return null;

  return (
    <div className="max-w-2xl mx-auto p-4">
      <div className="card bg-base-100 shadow-xl">
        <div className="card-body">
          <div className="flex items-center gap-4 mb-4">
            <div className="avatar">
              <div className="w-24 rounded-full ring ring-primary ring-offset-base-100 ring-offset-2">
                <img src={form.photo_url || "/avatar.png"} alt="Profile" />
              </div>
            </div>
            {editMode ? (
              <input type="file" accept="image/*" className="file-input file-input-bordered" onChange={handlePhotoChange} />
            ) : null}
            <div className="flex-1">
              <h2 className="card-title text-2xl">{profile.name}</h2>
              <p className="text-sm text-gray-500">{profile.email}</p>
            </div>
          </div>

          <div className="form-control mb-2">
            <label className="label">Availability</label>
            {editMode ? (
              <select name="availability" className="select select-bordered" value={form.availability || ""} onChange={handleChange}>
                <option value="">Select...</option>
                {AVAILABILITY_OPTIONS.map(opt => <option key={opt} value={opt}>{opt}</option>)}
              </select>
            ) : (
              <span className="badge badge-info badge-lg">{profile.availability || "Not set"}</span>
            )}
          </div>

          <div className="form-control mb-2">
            <label className="label">Skills Offered</label>
            {editMode ? (
              <input name="skills_offered" className="input input-bordered" value={form.skills_offered || ""} onChange={handleChange} placeholder="e.g. Python, React" />
            ) : (
              <span>{profile.skills_offered || "-"}</span>
            )}
          </div>

          <div className="form-control mb-2">
            <label className="label">Skills Wanted</label>
            {editMode ? (
              <input name="skills_wanted" className="input input-bordered" value={form.skills_wanted || ""} onChange={handleChange} placeholder="e.g. FastAPI, UI/UX" />
            ) : (
              <span>{profile.skills_wanted || "-"}</span>
            )}
          </div>

          <div className="form-control mb-2">
            <label className="cursor-pointer label">
              <span className="label-text">Public Profile</span>
              {editMode ? (
                <input type="checkbox" name="is_public" className="toggle toggle-primary ml-2" checked={!!form.is_public} onChange={handleChange} />
              ) : (
                <input type="checkbox" className="toggle toggle-primary ml-2" checked={!!profile.is_public} readOnly />
              )}
            </label>
          </div>

          <div className="card-actions mt-4 flex gap-2">
            {editMode ? (
              <>
                <button className="btn btn-primary" onClick={handleSave}>Save</button>
                <button className="btn btn-ghost" onClick={handleDiscard}>Discard</button>
              </>
            ) : (
              <button className="btn btn-secondary" onClick={() => setEditMode(true)}>Edit Profile</button>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}
