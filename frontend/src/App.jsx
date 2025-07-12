


import { BrowserRouter, Routes, Route } from "react-router-dom";
import AuthTabs from "./components/auth/AuthTabs";
import ProfileList from "./components/profiles/ProfileList";
import UserProfile from "./components/profile/UserProfile";

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={
          <main className="min-h-screen flex items-center justify-center bg-base-200">
            <AuthTabs />
          </main>
        } />
        <Route path="/profiles" element={<ProfileList />} />
        <Route path="/profile" element={<UserProfile />} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;
