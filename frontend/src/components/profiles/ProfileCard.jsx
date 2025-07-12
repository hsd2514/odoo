import React from "react";
import { Link } from "react-router-dom";

/**
 * ProfileCard - DaisyUI card for displaying a public user profile
 * Props: user (object with name, photo_url, skills, rating, etc.), onRequest (function)
 */


const ProfileCard = ({ user, onRequestSwap, onRequestInvite, currentUser }) => {
  try {
    if (!user || typeof user !== 'object') return null;
    return (
      <Link to={user.id ? `/profile/${user.id}` : "#"} className="card bg-base-100 shadow-md mb-4 hover:shadow-lg transition-shadow duration-150">
        <div className="card-body flex flex-row items-center gap-4 cursor-pointer">
          {/* Colorful DaisyUI avatar placeholder with initials */}
          {user.photo_url ? (
            <img
              src={user.photo_url}
              alt="Profile"
              className="rounded-full w-16 h-16 object-cover border"
            />
          ) : (
            <div
              className="avatar placeholder w-16 h-16 flex items-center justify-center rounded-full border text-white font-bold text-xl select-none"
              style={{ background: getColorFromName(user.name) }}
            >
              <span>{getInitials(user.name)}</span>
            </div>
          )}
          <div className="flex-1">
              <h3 className="font-bold text-lg">{user.name || "-"}</h3>
            <div className="text-sm text-gray-500">{user.location || "-"}</div>
            <div className="flex flex-wrap gap-2 mt-2">
              {(user.skills_offered || []).map((skill) => (
                <span key={skill} className="badge badge-outline badge-info">{skill}</span>
              ))}
            </div>
            <div className="flex flex-wrap gap-2 mt-1">
              {(user.skills_wanted || []).map((skill) => (
                <span key={skill} className="badge badge-outline badge-warning">{skill}</span>
              ))}
            </div>
            <div className="mt-2 text-xs">Rating: {user.rating ?? "-"}</div>
          </div>
          <div className="flex flex-col gap-2">
            <button className="btn btn-primary" onClick={e => { e.preventDefault(); onRequestSwap && onRequestSwap(user); }}>
              Request Swap
            </button>
            <button className="btn btn-secondary" onClick={e => { e.preventDefault(); onRequestInvite && onRequestInvite(user); }}>
              Request Invite
            </button>
          </div>
        </div>
      </Link>
    );
  } catch (err) {
    console.error("Error rendering ProfileCard", err, user);
    return <div className="alert alert-error">Profile error</div>;
  }
};

export default ProfileCard;
// Helper: Get initials from name
function getInitials(name) {
  if (!name) return "?";
  const parts = name.trim().split(" ");
  if (parts.length === 1) return parts[0][0].toUpperCase();
  return (parts[0][0] + parts[parts.length - 1][0]).toUpperCase();
}

// Helper: Generate a pastel color from name string
function getColorFromName(name) {
  // Simple hash to get a number from the name
  let hash = 0;
  for (let i = 0; i < (name || "?").length; i++) {
    hash = name.charCodeAt(i) + ((hash << 5) - hash);
  }
  // Generate HSL pastel color
  const hue = Math.abs(hash) % 360;
  return `hsl(${hue}, 70%, 70%)`;
}
