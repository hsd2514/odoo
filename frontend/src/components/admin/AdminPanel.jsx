import React, { useEffect, useState } from "react";
import axios from "axios";

/**
 * AdminPanel.jsx
 * Simple admin dashboard for user/skill/swap management and announcements.
 * For beginners: This fetches users, pending skills, and allows admin actions.
 */

export default function AdminPanel() {
  const [users, setUsers] = useState([]);
  const [pendingSkills, setPendingSkills] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [announcement, setAnnouncement] = useState("");
  const [message, setMessage] = useState("");

  // Fetch users and pending skills
  useEffect(() => {
    setLoading(true);
    Promise.all([
      axios.get("/admin/users"),
      axios.get("/admin/skills/pending"),
    ])
      .then(([usersRes, skillsRes]) => {
        setUsers(usersRes.data);
        setPendingSkills(skillsRes.data);
        setLoading(false);
      })
      .catch(() => {
        setError("Failed to load admin data");
        setLoading(false);
      });
  }, []);

  // Delete user
  function handleDeleteUser(id) {
    if (!window.confirm("Are you sure you want to ban/delete this user?")) return;
    axios.delete(`/admin/users/${id}`)
      .then(() => setUsers(users.filter(u => u.id !== id)))
      .catch(() => setMessage("Failed to delete user"));
  }

  // Remove skill (stub, implement endpoint if needed)
  function handleRemoveSkill(id) {
    setPendingSkills(pendingSkills.filter(s => s.id !== id));
    // TODO: Call backend endpoint to remove skill
  }

  // Broadcast announcement (stub, implement endpoint if needed)
  function handleBroadcast() {
    setMessage("Announcement sent (stub)");
    setAnnouncement("");
    // TODO: Call backend endpoint to broadcast
  }

  if (loading) return <div className="card bg-base-100 shadow p-4">Loading...</div>;
  if (error) return <div className="card bg-base-100 shadow p-4 text-error">{error}</div>;

  return (
    <div className="max-w-3xl mx-auto p-4">
      <div className="card bg-base-100 shadow-xl mb-4">
        <div className="card-body">
          <h3 className="card-title text-lg mb-2">Admin: Users</h3>
          <ul className="space-y-1">
            {users.map((user) => (
              <li key={user.id} className="flex items-center gap-2 justify-between">
                <span>{user.name} ({user.email})</span>
                <button className="btn btn-xs btn-error" onClick={() => handleDeleteUser(user.id)}>Ban/Delete</button>
              </li>
            ))}
          </ul>
        </div>
      </div>
      <div className="card bg-base-100 shadow-xl mb-4">
        <div className="card-body">
          <h3 className="card-title text-lg mb-2">Pending Skills</h3>
          <ul className="space-y-1">
            {pendingSkills.map((skill) => (
              <li key={skill.id} className="flex items-center gap-2 justify-between">
                <span>{skill.name} ({skill.category})</span>
                <button className="btn btn-xs btn-warning" onClick={() => handleRemoveSkill(skill.id)}>Remove</button>
              </li>
            ))}
          </ul>
        </div>
      </div>
      <div className="card bg-base-100 shadow-xl mb-4">
        <div className="card-body">
          <h3 className="card-title text-lg mb-2">Broadcast Announcement</h3>
          <div className="flex gap-2">
            <input
              className="input input-bordered flex-1"
              value={announcement}
              onChange={e => setAnnouncement(e.target.value)}
              placeholder="Type announcement..."
            />
            <button className="btn btn-primary" onClick={handleBroadcast}>Send</button>
          </div>
          {message && <div className="text-success mt-2">{message}</div>}
        </div>
      </div>
    </div>
  );
}
