




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
import InviteList from "./components/invites/InviteList";
import { AuthProvider, useAuth } from "./context/AuthContext";


import PublicUserProfile from "./components/profile/PublicUserProfile";




function AppRoutes() {
  const { user, logout } = useAuth();
  return (
    <BrowserRouter>
      <Navbar user={user} onLogout={logout} />
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
        <Route path="/profile/:id" element={<PublicUserProfile />} />

        {/* Swap Request Module */}
        <Route path="/swaps" element={<SwapRequestList />} />
        {/* Optionally, add a route for SwapRequestForm if you want a separate page */}
        {/* <Route path="/swaps/new" element={<SwapRequestForm />} /> */}
        <Route path="/invites" element={<InviteList />} />
      </Routes>
    </BrowserRouter>
  );
}

export default function App() {
  return (
    <AuthProvider>
      <AppRoutes />
    </AuthProvider>
  );
}


