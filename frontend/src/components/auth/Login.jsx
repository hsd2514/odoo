import React, { useState } from "react";
import { useNavigate } from "react-router-dom";

/**
 * Login component - DaisyUI card, email/password fields, login button, forgot password link
 * Matches Screen 2 of the mockup
 */
const Login = ({ onLogin }) => {
  const navigate = useNavigate();
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

  const [error, setError] = useState("");

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError("");
    try {
      const res = await fetch("http://localhost:8000/auth/login", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ email, password }),
      });
      if (!res.ok) throw new Error("Invalid credentials");
      const data = await res.json();
      localStorage.setItem("token", data.access_token);
      if (onLogin) onLogin(data);
      navigate("/profiles");
    } catch (err) {
      setError(err.message);
    }
  };

  return (
    <div className="card w-full max-w-sm bg-base-100 shadow-xl">
      <div className="card-body">
        <h2 className="card-title mb-2">Login</h2>
        <form onSubmit={handleSubmit} className="flex flex-col gap-4">
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
          <button type="submit" className="btn btn-primary w-full">Login</button>
          {error && <div className="text-error text-sm mt-2">{error}</div>}
        </form>
        <div className="mt-2 text-center">
          <a href="#" className="link link-hover text-sm">Forgot username/password?</a>
        </div>
      </div>
    </div>
  );
};

export default Login;
