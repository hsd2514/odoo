

import { BrowserRouter, Routes, Route } from "react-router-dom";
import AuthTabs from "./components/auth/AuthTabs";
import ProfileList from "./components/profiles/ProfileList";

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
      </Routes>
    </BrowserRouter>
  );
}

export default App;
