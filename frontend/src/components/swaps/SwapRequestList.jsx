import React, { useEffect, useState } from "react";
import axios from "axios";
import SwapRequestCard from "./SwapRequestCard";

/**
 * SwapRequestList.jsx
 * DaisyUI + Tailwind list of incoming/outgoing swap requests with status, accept/reject buttons.
 * For beginners: Shows all swap requests for the current user.
 */
export default function SwapRequestList() {
  const [requests, setRequests] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  function fetchRequests() {
    setLoading(true);
    axios.get("/swaps/requests")
      .then(res => {
        setRequests(res.data);
        setLoading(false);
      })
      .catch(() => {
        setError("Failed to load requests");
        setLoading(false);
      });
  }

  useEffect(() => {
    fetchRequests();
  }, []);

  function handleAccept(id) {
    axios.post(`/swaps/requests/${id}/accept`)
      .then(fetchRequests);
  }
  function handleReject(id) {
    axios.post(`/swaps/requests/${id}/reject`)
      .then(fetchRequests);
  }

  if (loading) return <div className="flex justify-center items-center h-32">Loading...</div>;
  if (error) return <div className="alert alert-error">{error}</div>;
  if (!requests.length) return <div className="text-center">No swap requests found.</div>;

  return (
    <div className="max-w-2xl mx-auto p-4">
      <h2 className="text-2xl font-bold mb-4">Swap Requests</h2>
      {requests.map(req => (
        <SwapRequestCard key={req.id} request={req} onAccept={handleAccept} onReject={handleReject} />
      ))}
    </div>
  );
}
