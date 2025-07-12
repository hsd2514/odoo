import React, { useEffect, useState, useContext } from "react";
import { AuthContext } from "../../context/AuthContext";
import axios from "axios";
import InviteCard from "./InviteCard";

const PAGE_SIZE = 5;

/**
 * InviteList.jsx
 * Shows a list of invites for the logged-in user.
 * Usage: <InviteList />
 */
export default function InviteList() {
  const { user } = useContext(AuthContext);
  const [incoming, setIncoming] = useState([]);
  const [outgoing, setOutgoing] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [page, setPage] = useState(1);

  const fetchInvites = () => {
    setLoading(true);
    Promise.all([
      axios.get(`/invites/incoming?page=${page}&page_size=${PAGE_SIZE}`),
      axios.get(`/invites/outgoing?page=${page}&page_size=${PAGE_SIZE}`)
    ])
      .then(([inRes, outRes]) => {
        setIncoming(inRes.data);
        setOutgoing(outRes.data);
        setError("");
      })
      .catch(() => setError("Failed to load invites"))
      .finally(() => setLoading(false));
  };

  useEffect(() => {
    fetchInvites();
  }, [page]);

  const handleAccept = (id) => {
    axios.put(`/invites/${id}`, { status: "accepted" })
      .then(fetchInvites);
  };
  const handleDecline = (id) => {
    axios.put(`/invites/${id}`, { status: "declined" })
      .then(fetchInvites);
  };
  const handleFeedback = (id, rating, feedback) => {
    axios.post(`/invites/${id}/feedback`, { rating, feedback })
      .then(fetchInvites);
  };

  return (
    <div className="max-w-2xl mx-auto p-4">
      <h2 className="text-2xl font-bold mb-4">My Invites</h2>
      {loading ? (
        <div className="loading loading-spinner loading-lg text-primary"></div>
      ) : error ? (
        <div className="alert alert-error">{error}</div>
      ) : (
        <>
          <h3 className="text-lg font-semibold mt-4 mb-2">Incoming Invites</h3>
          {incoming.length === 0 ? (
            <div className="alert alert-info mb-4">No incoming invites.</div>
          ) : (
            <div className="flex flex-col gap-4 mb-6">
              {incoming.map(invite => (
                <InviteCard
                  key={invite.id}
                  invite={invite}
                  direction="incoming"
                  currentUserId={user?.id}
                  onAccept={handleAccept}
                  onDecline={handleDecline}
                  onFeedback={handleFeedback}
                />
              ))}
            </div>
          )}
          <h3 className="text-lg font-semibold mt-4 mb-2">Outgoing Invites</h3>
          {outgoing.length === 0 ? (
            <div className="alert alert-info">No outgoing invites.</div>
          ) : (
            <div className="flex flex-col gap-4">
              {outgoing.map(invite => (
                <InviteCard
                  key={invite.id}
                  invite={invite}
                  direction="outgoing"
                  currentUserId={user?.id}
                  onAccept={() => {}}
                  onDecline={() => {}}
                  onFeedback={handleFeedback}
                />
              ))}
            </div>
          )}
          <div className="flex justify-center mt-4 gap-2">
            {[1,2,3,4,5].map(p => (
              <button key={p} className={`btn btn-sm ${p===page ? "btn-primary" : "btn-outline"}`} onClick={() => setPage(p)}>{p}</button>
            ))}
          </div>
        </>
      )}
    </div>
  );
}
