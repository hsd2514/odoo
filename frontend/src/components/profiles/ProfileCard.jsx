import React from "react";

/**
 * ProfileCard - DaisyUI card for displaying a public user profile
 * Props: user (object with name, photo_url, skills, rating, etc.), onRequest (function)
 */


const ProfileCard = ({ user, onRequestSwap, onRequestInvite, currentUser }) => {
  // Simple compatibility: percent of overlap between currentUser's wanted and user's offered, and vice versa
  function getMatchScore() {
    if (!currentUser) return null;
    const offered = new Set(user.skills_offered || []);
    const wanted = new Set(user.skills_wanted || []);
    const myOffered = new Set(currentUser.skills_offered || []);
    const myWanted = new Set(currentUser.skills_wanted || []);
    // Offered-to-wanted match
    const match1 = [...myWanted].filter(skill => offered.has(skill)).length;
    const match2 = [...wanted].filter(skill => myOffered.has(skill)).length;
    const total = (myWanted.size + myOffered.size) || 1;
    let score = Math.round(((match1 + match2) / total) * 100);
    // Bonus if availability matches
    if (user.availability && currentUser.availability && user.availability === currentUser.availability) score += 10;
    if (score > 100) score = 100;
    return score;
  }
  const matchScore = getMatchScore();
  return (
    <div className="card bg-base-100 shadow-md mb-4">
      <div className="card-body flex flex-row items-center gap-4">
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
            style={{
              background: getColorFromName(user.name)
            }}
          >
            <span>{getInitials(user.name)}</span>
          </div>
        )}
        <div className="flex-1">
          <h3 className="font-bold text-lg flex items-center gap-2">{user.name}
            {matchScore !== null && (
              <span className="badge badge-success badge-outline ml-2">{matchScore}% Match</span>
            )}
          </h3>
          <div className="text-sm text-gray-500">{user.location}</div>
          <div className="flex flex-wrap gap-2 mt-2">
            {user.skills_offered?.map((skill) => (
              <span key={skill} className="badge badge-outline badge-info">{skill}</span>
            ))}
          </div>
          <div className="flex flex-wrap gap-2 mt-1">
            {user.skills_wanted?.map((skill) => (
              <span key={skill} className="badge badge-outline badge-warning">{skill}</span>
            ))}
          </div>
          <div className="mt-2 text-xs">Rating: {user.rating ?? "-"}</div>
        </div>
        <div className="flex flex-col gap-2">
          <button className="btn btn-primary" onClick={() => onRequestSwap(user)}>
            Request Swap
          </button>
          <button className="btn btn-secondary" onClick={() => onRequestInvite(user)}>
            Request Invite
          </button>
        </div>
      </div>
    </div>
  );
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
