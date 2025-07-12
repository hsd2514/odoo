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
  // Theme toggle handler (button)
  const [theme, setTheme] = React.useState(() =>
    document.querySelector("html").getAttribute("data-theme") || "light"
  );
  const toggleTheme = () => {
    const newTheme = theme === "light" ? "dark" : "light";
    setTheme(newTheme);
    document.querySelector("html").setAttribute("data-theme", newTheme);
  };
  return (
    <div className="navbar bg-base-100 shadow mb-4">
      <div className="flex-1">
        <Link to="/" className="btn btn-ghost normal-case text-xl">Skill Swap Platform</Link>
      </div>
      <div className="flex-none gap-2 items-center">
        <button
          className="btn btn-sm btn-outline"
          onClick={toggleTheme}
          aria-label="Toggle theme"
        >
          {theme === "light" ? "🌞 Light" : "🌙 Dark"}
        </button>
        <Link to="/profiles" className="btn btn-ghost">Home</Link>
        <Link to="/swaps" className="btn btn-ghost">Swap Requests</Link>
        <Link to="/invites" className="btn btn-ghost">My Invites</Link>
        {user ? (
          <>
            <div className="avatar cursor-pointer" onClick={() => navigate("/profile")}> 
              <div className="w-10 rounded-full flex items-center justify-center bg-base-200">
                {user.photo_url ? (
                  <img src={user.photo_url} alt="Profile" />
                ) : (
                  <span
                    className="w-full h-full flex items-center justify-center text-white font-bold text-lg select-none"
                    style={{ background: getColorFromName(user.name) }}
                  >
                    {getInitials(user.name)}
                  </span>
                )}
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

// Helper: Get initials from name
function getInitials(name) {
  if (!name) return "?";
  const parts = name.trim().split(" ");
  if (parts.length === 1) return parts[0][0].toUpperCase();
  return (parts[0][0] + parts[parts.length - 1][0]).toUpperCase();
}

// Helper: Generate a pastel color from name string
function getColorFromName(name) {
  let hash = 0;
  for (let i = 0; i < (name || "?").length; i++) {
    hash = name.charCodeAt(i) + ((hash << 5) - hash);
  }
  const hue = Math.abs(hash) % 360;
  return `hsl(${hue}, 70%, 70%)`;
}
