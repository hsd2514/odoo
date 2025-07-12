import React, { useState, useEffect } from "react";
import axios from "axios";

axios.defaults.baseURL = "http://localhost:8000";

/**
 * UserProfile.jsx
 * DaisyUI + Tailwind user profile page with edit/save/discard, skills, availability, public/private toggle, and profile photo.
 * For beginners: This component fetches the current user's profile, allows editing, and updates the backend.
 */

const AVAILABILITY_OPTIONS = ["Available", "Busy", "Looking for Opportunities"];

// Helper: get initials from name
function getInitials(name) {
  if (!name) return "";
  return name
    .split(" ")
    .map((n) => n[0])
    .join("")
    .toUpperCase();
}

// Helper: get color from name (for avatar background)
function getColorFromName(name) {
  if (!name) return "#888";
  let hash = 0;
  for (let i = 0; i < name.length; i++) {
    hash = name.charCodeAt(i) + ((hash << 5) - hash);
  }
  const color = `hsl(${hash % 360}, 70%, 60%)`;
  return color;
}

// Helper: badge color
function getBadgeColor(type) {
  switch (type) {
    case "MENTOR":
      return "badge-primary";
    case "VOLUNTEER":
      return "badge-secondary";
    case "ORGANIZER":
      return "badge-accent";
    default:
      return "badge-neutral";
  }
}

export default function UserProfile() {
  const [profile, setProfile] = useState({});
  const [editMode, setEditMode] = useState(false);
  const [form, setForm] = useState({});
  const [badges, setBadges] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  // Fetch profile and badges on mount
  useEffect(() => {
    axios
      .get("/users/me")
      .then((res) => {
        // Convert skills_offered/wanted to comma string for input
        const data = {
          ...res.data,
          skills_offered: Array.isArray(res.data.skills_offered)
            ? res.data.skills_offered.join(", ")
            : res.data.skills_offered || "",
          skills_wanted: Array.isArray(res.data.skills_wanted)
            ? res.data.skills_wanted.join(", ")
            : res.data.skills_wanted || "",
        };
        setProfile(data);
        setForm(data);
        setLoading(false);
        // Fetch badges for this user
        if (res.data?.id) {
          axios
            .get(`/badges/user/${res.data.id}`)
            .then((badgeRes) => setBadges(badgeRes.data))
            .catch(() => setBadges([]));
        }
      })
      .catch(() => {
        setError("Failed to load profile");
        setLoading(false);
      });
  }, []);

  // Handle form changes
  function handleChange(e) {
    const { name, value, type, checked } = e.target;
    setForm((f) => ({
      ...f,
      [name]: type === "checkbox" ? checked : value,
    }));
  }

  // Handle photo upload (stub for beginners)
  function handlePhotoChange(e) {
    // For beginners: In a real app, upload the file and set photo_url.
    // Here, just show a preview.
    const file = e.target.files[0];
    if (file) {
      const reader = new FileReader();
      reader.onload = (ev) => {
        setForm((f) => ({
          ...f,
          photo_url: ev.target.result,
        }));
      };
      reader.readAsDataURL(file);
    }
  }

  // Discard changes
  function handleDiscard() {
    setForm(profile);
    setEditMode(false);
  }

  // Save profile
  function handleSave() {
    setLoading(true);
    // Only send fields expected by backend schema
    const payload = {
      name: form.name,
      location: form.location,
      availability: form.availability,
      is_public: form.is_public,
      photo_url: form.photo_url,
      // Convert comma string to array for backend
      skills_offered: form.skills_offered
        ? form.skills_offered.split(",").map((s) => s.trim()).filter(Boolean)
        : [],
      skills_wanted: form.skills_wanted
        ? form.skills_wanted.split(",").map((s) => s.trim()).filter(Boolean)
        : [],
    };
    axios
      .put("/users/me", payload)
      .then((res) => {
        setProfile({
          ...res.data,
          skills_offered: Array.isArray(res.data.skills_offered)
            ? res.data.skills_offered.join(", ")
            : res.data.skills_offered || "",
          skills_wanted: Array.isArray(res.data.skills_wanted)
            ? res.data.skills_wanted.join(", ")
            : res.data.skills_wanted || "",
        });
        setEditMode(false);
        setLoading(false);
        setError("");
      })
      .catch(() => {
        setError("Failed to save profile");
        setLoading(false);
      });
  }

  if (loading) {
    return (
      <div className="flex justify-center items-center h-40">
        <span className="loading loading-spinner loading-lg"></span>
      </div>
    );
  }

  if (error) {
    return (
      <div className="alert alert-error">
        <span>{error}</span>
      </div>
    );
  }

  return (
    <div className="max-w-2xl mx-auto p-4">
      <div className="card bg-base-100 shadow-xl">
        <div className="card-body">
          <div className="flex items-center gap-4 mb-4">
            <div className="avatar">
              <div className="w-24 rounded-full ring ring-primary ring-offset-base-100 ring-offset-2 flex items-center justify-center bg-base-200">
                {form.photo_url ? (
                  <img src={form.photo_url} alt="Profile" />
                ) : (
                  <span
                    className="w-full h-full flex items-center justify-center text-white font-bold text-3xl select-none"
                    style={{ background: getColorFromName(form.name) }}
                  >
                    {getInitials(form.name)}
                  </span>
                )}
              </div>
            </div>
            <div className="flex-1">
              <h2 className="card-title text-2xl">{profile.name}</h2>
              <p className="text-sm text-gray-500">{profile.email}</p>
              {/* Badges section */}
              {badges.length > 0 && (
                <div className="mt-2 flex flex-wrap gap-2">
                  {badges.map((badge) => (
                    <span
                      key={badge.id}
                      className={`badge badge-outline ${getBadgeColor(
                        badge.badge_type
                      )}`}
                      title={badge.badge_type}
                    >
                      {badge.badge_type.replace(/_/g, " ")}
                    </span>
                  ))}
                </div>
              )}
            </div>
            {editMode ? (
              <input
                type="file"
                accept="image/*"
                className="file-input file-input-bordered"
                onChange={handlePhotoChange}
              />
            ) : null}
          </div>
          {/* Availability */}
          <div className="form-control mb-2">
            <label className="label">Availability</label>
            {editMode ? (
              <select
                name="availability"
                className="select select-bordered"
                value={form.availability || ""}
                onChange={handleChange}
              >
                <option value="">Select...</option>
                {AVAILABILITY_OPTIONS.map((opt) => (
                  <option key={opt} value={opt}>
                    {opt}
                  </option>
                ))}
              </select>
            ) : (
              <span className="badge badge-info badge-lg">
                {profile.availability || "Not set"}
              </span>
            )}
          </div>
          {/* Location */}
          <div className="form-control mb-2">
            <label className="label">Location</label>
            {editMode ? (
              <input
                name="location"
                className="input input-bordered"
                value={form.location || ""}
                onChange={handleChange}
                placeholder="e.g. Bangalore"
              />
            ) : (
              <span>{profile.location || "-"}</span>
            )}
          </div>
          {/* Skills Offered */}
          <div className="form-control mb-2">
            <label className="label">Skills Offered</label>
            {editMode ? (
              <input
                name="skills_offered"
                className="input input-bordered"
                value={form.skills_offered || ""}
                onChange={handleChange}
                placeholder="e.g. Python, React"
              />
            ) : (
              <span>
                {profile.skills_offered
                  ? profile.skills_offered
                  : "-"}
              </span>
            )}
          </div>
          {/* Skills Wanted */}
          <div className="form-control mb-2">
            <label className="label">Skills Wanted</label>
            {editMode ? (
              <input
                name="skills_wanted"
                className="input input-bordered"
                value={form.skills_wanted || ""}
                onChange={handleChange}
                placeholder="e.g. FastAPI, UI/UX"
              />
            ) : (
              <span>
                {profile.skills_wanted
                  ? profile.skills_wanted
                  : "-"}
              </span>
            )}
          </div>
          {/* Public Profile Toggle */}
          <div className="form-control mb-2">
            <label className="cursor-pointer label">
              <span className="label-text">Public Profile</span>
              {editMode ? (
                <input
                  type="checkbox"
                  name="is_public"
                  className="toggle toggle-primary ml-2"
                  checked={!!form.is_public}
                  onChange={handleChange}
                />
              ) : (
                <input
                  type="checkbox"
                  className="toggle toggle-primary ml-2"
                  checked={!!profile.is_public}
                  readOnly
                />
              )}
            </label>
          </div>
          <div className="card-actions mt-4 flex gap-2">
            {editMode ? (
              <>
                <button className="btn btn-primary" onClick={handleSave}>
                  Save
                </button>
                <button className="btn btn-ghost" onClick={handleDiscard}>
                  Discard
                </button>
              </>
            ) : (
              <button
                className="btn btn-secondary"
                onClick={() => setEditMode(true)}
              >
                Edit Profile
              </button>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}
