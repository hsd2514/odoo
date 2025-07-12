import React, { useEffect, useState } from "react";
import axios from "axios";
import SwapRequestCard from "./SwapRequestCard";

const PAGE_SIZE = 5;

/**
 * SwapRequestList.jsx
 * DaisyUI + Tailwind list of incoming/outgoing swap requests with status, accept/reject buttons.
 * For beginners: Shows all swap requests for the current user.
 */
export default function SwapRequestList() {
  const [incoming, setIncoming] = useState([]);
  const [outgoing, setOutgoing] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [page, setPage] = useState(1);

  // Fetch both incoming and outgoing swap requests
  function fetchRequests() {
    setLoading(true);
    Promise.all([
      axios.get(`/swaps/incoming?page=${page}&page_size=${PAGE_SIZE}`),
      axios.get(`/swaps/outgoing?page=${page}&page_size=${PAGE_SIZE}`)
    ])
      .then(([inRes, outRes]) => {
        setIncoming(inRes.data);
        setOutgoing(outRes.data);
        setLoading(false);
      })
      .catch(() => {
        setError("Failed to load requests");
        setLoading(false);
      });
  }

  useEffect(() => {
    fetchRequests();
  }, [page]);

  function handleAccept(id) {
    axios.put(`/swaps/${id}`, { status: "accepted" })
      .then(fetchRequests);
  }
  function handleReject(id) {
    axios.put(`/swaps/${id}`, { status: "rejected" })
      .then(fetchRequests);
  }

  // Feedback/rating submission (dummy for hackathon)
  function handleFeedback(id, rating, feedback) {
    axios.post(`/swaps/${id}/feedback`, { rating, feedback })
      .then(fetchRequests);
  }

  if (loading) return <div className="flex justify-center items-center h-32">Loading...</div>;
  if (error) return <div className="alert alert-error">{error}</div>;

  return (
    <div className="max-w-2xl mx-auto p-4">
      <h2 className="text-2xl font-bold mb-4">Swap Requests</h2>
      <h3 className="text-lg font-semibold mt-4 mb-2">Incoming Requests</h3>
      {incoming.length === 0 ? (
        <div className="alert alert-info mb-4">No incoming requests.</div>
      ) : (
        <div className="flex flex-col gap-4 mb-6">
          {incoming.map(req => (
            <SwapRequestCard key={req.id} request={req} onAccept={handleAccept} onReject={handleReject} onFeedback={handleFeedback} />
          ))}
        </div>
      )}
      <h3 className="text-lg font-semibold mt-4 mb-2">Outgoing Requests</h3>
      {outgoing.length === 0 ? (
        <div className="alert alert-info">No outgoing requests.</div>
      ) : (
        <div className="flex flex-col gap-4">
          {outgoing.map(req => (
            <SwapRequestCard key={req.id} request={req} onAccept={() => {}} onReject={() => {}} onFeedback={handleFeedback} />
          ))}
        </div>
      )}
      <div className="flex justify-center mt-4 gap-2 flex-wrap">
        {[1,2,3,4,5].map(p => (
          <button key={p} className={`btn btn-sm ${p===page ? "btn-primary" : "btn-outline"}`} onClick={() => setPage(p)}>{p}</button>
        ))}
      </div>
    </div>
  );
}
