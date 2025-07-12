




import { BrowserRouter, Routes, Route } from "react-router-dom";
import AuthTabs from "./components/auth/AuthTabs";
import ProfileList from "./components/profiles/ProfileList";
import ProfileCard from "./components/profiles/ProfileCard";
import SearchBar from "./components/profiles/SearchBar";
import Pagination from "./components/profiles/Pagination";
import UserProfile from "./components/profile/UserProfile";
import SwapRequestList from "./components/swaps/SwapRequestList";
import SwapRequestForm from "./components/swaps/SwapRequestForm";
import SwapRequestCard from "./components/swaps/SwapRequestCard";
import Navbar from "./components/shared/Navbar";
import { useState } from "react";



function App() {
  // Dummy user state for demo; replace with real auth logic
  const [user, setUser] = useState({ name: "Demo User", photo_url: "" });
  function handleLogout() {
    setUser(null);
    // Add real logout logic here
  }

  // Example: pass ProfileCard, SearchBar, Pagination to ProfileList for modularity
  // (Assumes ProfileList is set up to accept these as props; if not, update ProfileList accordingly)
  return (
    <BrowserRouter>
      <Navbar user={user} onLogout={handleLogout} />
      <Routes>
        {/* Auth Module */}
        <Route path="/" element={
          <main className="min-h-screen flex items-center justify-center bg-base-200">
            <AuthTabs />
          </main>
        } />

        {/* Home/Profiles Module */}
        <Route path="/profiles" element={<ProfileList ProfileCard={ProfileCard} SearchBar={SearchBar} Pagination={Pagination} />} />

        {/* Profile Module */}
        <Route path="/profile" element={<UserProfile />} />

        {/* Swap Request Module */}
        <Route path="/swaps" element={<SwapRequestList />} />
        {/* Optionally, add a route for SwapRequestForm if you want a separate page */}
        {/* <Route path="/swaps/new" element={<SwapRequestForm />} /> */}
      </Routes>
    </BrowserRouter>
  );
}

export default App;
