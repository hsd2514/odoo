
import React, { useState, useEffect, useContext } from "react";
import axios from "axios";
import { AuthContext } from "../../context/AuthContext";
import { useParams } from "react-router-dom";

/**
 * PublicUserProfile - Shows another user's profile and allows swap/invite requests
 */

const PublicUserProfile = () => {
  const { id } = useParams();
  const { user: currentUser } = useContext(AuthContext);
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [swapStatus, setSwapStatus] = useState("");
  const [inviteStatus, setInviteStatus] = useState("");
  // For skill selection (optional, use first skill by default)
  const [selectedOffered, setSelectedOffered] = useState("");
  const [selectedRequested, setSelectedRequested] = useState("");
  const [selectedInviteSkill, setSelectedInviteSkill] = useState("");

  useEffect(() => {
    setLoading(true);
    axios.get(`/users/${id}`)
      .then(res => {
        setUser(res.data);
        setLoading(false);
        // Set sensible defaults for skill selection
        setSelectedOffered(currentUser?.skills_offered?.[0] || "");
        setSelectedRequested(res.data.skills_offered?.[0] || "");
        setSelectedInviteSkill(res.data.skills_offered?.[0] || "");
      })
      .catch(err => {
        if (err.response && err.response.status === 404) {
          setError("User not found or not public.");
        } else {
          setError("An error occurred loading the profile.");
        }
        setLoading(false);
      });
  }, [id, currentUser]);

  // Request a swap (POST /swaps/)
  const handleRequestSwap = async () => {
    setSwapStatus("");
    if (!selectedOffered || !selectedRequested) {
      setSwapStatus("Please select both skills.");
      return;
    }
    try {
      await axios.post("/api/swaps/", {
        receiver_id: user.id,
        skill_offered: selectedOffered,
        skill_requested: selectedRequested,
      });
      setSwapStatus("Swap request sent!");
    } catch (err) {
      setSwapStatus("Error sending swap request");
    }
  };

  // Request an invite (POST /invites/)
  const handleRequestInvite = async () => {
    setInviteStatus("");
    if (!selectedInviteSkill) {
      setInviteStatus("Please select a skill.");
      return;
    }
    try {
      await axios.post("/api/invites/", {
        receiver_id: user.id,
        skill_id: selectedInviteSkill,
      });
      setInviteStatus("Invite request sent!");
    } catch (err) {
      setInviteStatus("Error sending invite request");
    }
  };

  if (loading) return <div className="loading loading-spinner">Loading...</div>;
  if (error) return <div className="alert alert-error">{error}</div>;
  if (!user) return null;

  return (
    <div className="max-w-xl mx-auto card bg-base-100 shadow-lg mt-8 p-6">
      <div className="flex items-center gap-6">
        {user.photo_url ? (
          <img src={user.photo_url} alt="Profile" className="rounded-full w-24 h-24 object-cover border" />
        ) : (
          <div className="avatar placeholder w-24 h-24 flex items-center justify-center rounded-full border text-white font-bold text-3xl select-none" style={{ background: getColorFromName(user.name) }}>
            <span>{getInitials(user.name)}</span>
          </div>
        )}
        <div>
          <h2 className="font-bold text-2xl">{user.name}</h2>
          <div className="text-gray-500">{user.location || "-"}</div>
          <div className="mt-2 text-xs">Rating: {user.rating ?? "-"}</div>
        </div>
      </div>
      <div className="mt-6">
        <div className="font-semibold mb-1">Skills Offered:</div>
        <div className="flex flex-wrap gap-2">
          {(user.skills_offered || []).map(skill => (
            <span key={skill} className="badge badge-info badge-outline">{skill}</span>
          ))}
        </div>
        <div className="font-semibold mt-4 mb-1">Skills Wanted:</div>
        <div className="flex flex-wrap gap-2">
          {(user.skills_wanted || []).map(skill => (
            <span key={skill} className="badge badge-warning badge-outline">{skill}</span>
          ))}
        </div>
      </div>
      <div className="divider" />
      <div className="flex flex-col md:flex-row gap-4 mt-4">
        <div className="flex-1">
          <div className="font-semibold mb-1">Request a Swap</div>
          <div className="flex gap-2 mb-2">
            <select className="select select-bordered" value={selectedOffered} onChange={e => setSelectedOffered(e.target.value)}>
              <option value="">Your Skill to Offer</option>
              {(currentUser?.skills_offered || []).map(skill => (
                <option key={skill} value={skill}>{skill}</option>
              ))}
            </select>
            <select className="select select-bordered" value={selectedRequested} onChange={e => setSelectedRequested(e.target.value)}>
              <option value="">Their Skill to Request</option>
              {(user.skills_offered || []).map(skill => (
                <option key={skill} value={skill}>{skill}</option>
              ))}
            </select>
            <button className="btn btn-primary" onClick={handleRequestSwap}>Request Swap</button>
          </div>
          {swapStatus && <div className="text-xs mt-1 text-info">{swapStatus}</div>}
        </div>
        <div className="flex-1">
          <div className="font-semibold mb-1">Request an Invite</div>
          <div className="flex gap-2 mb-2">
            <select className="select select-bordered" value={selectedInviteSkill} onChange={e => setSelectedInviteSkill(e.target.value)}>
              <option value="">Their Skill</option>
              {(user.skills_offered || []).map(skill => (
                <option key={skill} value={skill}>{skill}</option>
              ))}
            </select>
            <button className="btn btn-secondary" onClick={handleRequestInvite}>Request Invite</button>
          </div>
          {inviteStatus && <div className="text-xs mt-1 text-info">{inviteStatus}</div>}
        </div>
      </div>
    </div>
  );
};

export default PublicUserProfile;

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
