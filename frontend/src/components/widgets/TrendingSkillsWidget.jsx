import React, { useEffect, useState } from "react";
import axios from "axios";

/**
 * TrendingSkillsWidget.jsx
 * DaisyUI card showing top 3 trending skills (offered/requested most).
 * For beginners: This fetches trending skills from the backend and displays them.
 */

export default function TrendingSkillsWidget({ limit = 3 }) {
  const [skills, setSkills] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    axios
      .get(`/skills/trending?limit=${limit}`)
      .then((res) => {
        setSkills(res.data);
        setLoading(false);
      })
      .catch(() => {
        setError("Failed to load trending skills");
        setLoading(false);
      });
  }, [limit]);

  if (loading) return <div className="card bg-base-100 shadow p-4">Loading...</div>;
  if (error) return <div className="card bg-base-100 shadow p-4 text-error">{error}</div>;

  return (
    <div className="card bg-base-100 shadow-xl">
      <div className="card-body">
        <h3 className="card-title text-lg mb-2">Trending Skills</h3>
        <ul className="space-y-1">
          {skills.slice(0, limit).map((skill, idx) => (
            <li key={skill.id} className="flex items-center gap-2">
              <span className="badge badge-primary badge-sm">#{idx + 1}</span>
              <span className="font-semibold">{skill.name}</span>
              <span className="text-xs text-gray-500">({skill.category})</span>
            </li>
          ))}
        </ul>
      </div>
    </div>
  );
}
