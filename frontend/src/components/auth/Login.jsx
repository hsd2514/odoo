import React, { useState } from "react";

/**
 * Login component - DaisyUI card, email/password fields, login button, forgot password link
 * Matches Screen 2 of the mockup
 */
const Login = ({ onLogin }) => {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

  const handleSubmit = (e) => {
    e.preventDefault();
    // Example: Call backend API here
    if (onLogin) onLogin({ email, password });
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
        </form>
        <div className="mt-2 text-center">
          <a href="#" className="link link-hover text-sm">Forgot username/password?</a>
        </div>
      </div>
    </div>
  );
};

export default Login;
