import React from "react";

/**
 * ProfileCard - DaisyUI card for displaying a public user profile
 * Props: user (object with name, photo_url, skills, rating, etc.), onRequest (function)
 */

const ProfileCard = ({ user, onRequestSwap }) => (
  <div className="card bg-base-100 shadow-md mb-4">
    <div className="card-body flex flex-row items-center gap-4">
      <img
        src={user.photo_url || "https://placehold.co/64x64"}
        alt="Profile"
        className="rounded-full w-16 h-16 object-cover border"
      />
      <div className="flex-1">
        <h3 className="font-bold text-lg">{user.name}</h3>
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
      <button className="btn btn-primary" onClick={() => onRequestSwap(user)}>
        Request Swap
      </button>
    </div>
  </div>
);

export default ProfileCard;
