import React from "react";
import { Link, useNavigate } from "react-router-dom";

/**
 * Navbar.jsx
 * DaisyUI + Tailwind top navigation bar for Skill Swap Platform.
 * Shows: Brand, Home, Swap Requests, Profile Photo, Login/Logout.
 * For beginners: Use this at the top of your app for navigation.
 */
export default function Navbar({ user, onLogout }) {
  const navigate = useNavigate();
  return (
    <div className="navbar bg-base-100 shadow mb-4">
      <div className="flex-1">
        <Link to="/" className="btn btn-ghost normal-case text-xl">Skill Swap Platform</Link>
      </div>
      <div className="flex-none gap-2">
        <Link to="/profiles" className="btn btn-ghost">Home</Link>
        <Link to="/swaps" className="btn btn-ghost">Swap Requests</Link>
        {user ? (
          <>
            <div className="avatar cursor-pointer" onClick={() => navigate("/profile")}> 
              <div className="w-10 rounded-full">
                <img src={user.photo_url || "/avatar.png"} alt="Profile" />
              </div>
            </div>
            <button className="btn btn-outline ml-2" onClick={onLogout}>Logout</button>
          </>
        ) : (
          <Link to="/" className="btn btn-primary">Login</Link>
        )}
      </div>
    </div>
  );
}
