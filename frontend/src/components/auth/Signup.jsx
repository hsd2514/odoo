import React, { useState } from "react";

/**
 * Signup component - DaisyUI card, email/password/confirm fields, signup button
 * Matches Screen 2 style from the mockup
 */
const Signup = ({ onSignup }) => {
  const [name, setName] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [confirm, setConfirm] = useState("");
  const [location, setLocation] = useState("");
  const [availability, setAvailability] = useState("");
  const [isPublic, setIsPublic] = useState(true);

  const [error, setError] = useState("");
  const [success, setSuccess] = useState("");

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError("");
    setSuccess("");
    if (password !== confirm) {
      setError("Passwords do not match");
      return;
    }
    try {
      const res = await fetch("http://localhost:8000/auth/register", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          name,
          email,
          password,
          location,
          availability,
          is_public: isPublic,
        }),
      });
      if (!res.ok) throw new Error("Registration failed");
      setSuccess("Registration successful!");
      setName("");
      setEmail("");
      setPassword("");
      setConfirm("");
      setLocation("");
      setAvailability("");
      setIsPublic(true);
      if (onSignup) onSignup();
    } catch (err) {
      setError(err.message);
    }
  };

  return (
    <div className="card w-full max-w-sm bg-base-100 shadow-xl">
      <div className="card-body">
        <h2 className="card-title mb-2">Sign Up</h2>
        <form onSubmit={handleSubmit} className="flex flex-col gap-4">
          <input
            type="text"
            placeholder="Name"
            className="input input-bordered w-full"
            value={name}
            onChange={(e) => setName(e.target.value)}
            required
          />
          <input
            type="email"
            placeholder="Email"
            className="input input-bordered w-full"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            required
          />
          <input
            type="password"
            placeholder="Password"
            className="input input-bordered w-full"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
          />
          <input
            type="password"
            placeholder="Confirm Password"
            className="input input-bordered w-full"
            value={confirm}
            onChange={(e) => setConfirm(e.target.value)}
            required
          />
          <input
            type="text"
            placeholder="Location"
            className="input input-bordered w-full"
            value={location}
            onChange={(e) => setLocation(e.target.value)}
          />
          <input
            type="text"
            placeholder="Availability (e.g. weekends)"
            className="input input-bordered w-full"
            value={availability}
            onChange={(e) => setAvailability(e.target.value)}
          />
          <label className="flex items-center gap-2">
            <input
              type="checkbox"
              checked={isPublic}
              onChange={(e) => setIsPublic(e.target.checked)}
            />
            Public Profile
          </label>
          <button type="submit" className="btn btn-secondary w-full">Sign Up</button>
          {error && <div className="text-error text-sm mt-2">{error}</div>}
          {success && <div className="text-success text-sm mt-2">{success}</div>}
        </form>
      </div>
    </div>
  );
};

export default Signup;
