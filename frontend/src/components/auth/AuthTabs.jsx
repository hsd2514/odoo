import React, { useState } from "react";
import Login from "./Login";
import Signup from "./Signup";

/**
 * AuthTabs - Tab switcher for Login/Signup, DaisyUI card, matches mockup style
 */
const AuthTabs = () => {
  const [activeTab, setActiveTab] = useState("login");
  return (
    <div className="flex items-center justify-center min-h-screen bg-base-200">
      <div className="card w-full max-w-md shadow-xl bg-base-100">
        <div role="tablist" className="tabs tabs-boxed justify-center mt-4">
          <button
            role="tab"
            className={`tab ${activeTab === 'login' ? 'tab-active' : ''}`}
            onClick={() => setActiveTab('login')}
          >
            Login
          </button>
          <button
            role="tab"
            className={`tab ${activeTab === 'signup' ? 'tab-active' : ''}`}
            onClick={() => setActiveTab('signup')}
          >
            Sign Up
          </button>
        </div>
        <div className="card-body p-6">
          {activeTab === 'login' ? <Login /> : <Signup />}
        </div>
      </div>
    </div>
  );
};

export default AuthTabs;
