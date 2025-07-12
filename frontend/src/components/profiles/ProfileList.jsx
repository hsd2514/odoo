import React, { useState, useEffect } from "react";
import ProfileCard from "./ProfileCard";
import SearchBar from "./SearchBar";
import Pagination from "./Pagination";
import CategoryLocationFilter from "./CategoryLocationFilter";
import SwapRequestModal from "../swaps/SwapRequestModal";

/**
 * ProfileList - Displays paginated public profiles with search and filter
 */

const ProfileList = () => {
  const [profiles, setProfiles] = useState([]);
  const [swapModalOpen, setSwapModalOpen] = useState(false);
  const [selectedUser, setSelectedUser] = useState(null);
  const [search, setSearch] = useState("");
  const [availability, setAvailability] = useState("");
  const [category, setCategory] = useState("");
  const [location, setLocation] = useState("");
  const [categories, setCategories] = useState([]);
  const [locations, setLocations] = useState([]);
  const [page, setPage] = useState(1);
  const [totalPages, setTotalPages] = useState(1);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [filterLoading, setFilterLoading] = useState(false);
  const [filterError, setFilterError] = useState("");
  const pageSize = 10;

  // Set DaisyUI theme to light by default
  useEffect(() => {
    document.querySelector("html").setAttribute("data-theme", "light");
  }, []);

  const fetchProfiles = async () => {
    setLoading(true);
    setError("");
    try {
      const params = new URLSearchParams({
        ...(search && { search }),
        ...(availability && { availability }),
        ...(category && { category }),
        ...(location && { location }),
        page,
        page_size: pageSize,
      });
      const res = await fetch(`http://localhost:8000/users/public?${params}`);
      if (!res.ok) throw new Error("Failed to fetch profiles");
      const data = await res.json();
      setProfiles(data);
      setTotalPages(5); // TODO: Replace with real total pages if available
    } catch (err) {
      setError(err.message || "Error loading profiles");
    } finally {
      setLoading(false);
    }
  };

  // Fetch categories and locations for filters
  useEffect(() => {
    setFilterLoading(true);
    setFilterError("");
    Promise.all([
      fetch("http://localhost:8000/skills/categories").then(res => res.json()),
      fetch("http://localhost:8000/users/locations").then(res => res.json()),
    ])
      .then(([cats, locs]) => {
        setCategories(cats);
        setLocations(locs);
      })
      .catch(() => setFilterError("Failed to load filter options"))
      .finally(() => setFilterLoading(false));
  }, []);

  useEffect(() => {
    fetchProfiles();
    // eslint-disable-next-line
  }, [search, availability, category, location, page]);

  return (
    <div className="min-h-screen bg-base-200 flex flex-col items-center py-4 px-2 sm:px-0">
      <div className="w-full max-w-2xl">
        <div className="card bg-base-100 shadow-xl p-4 mb-4">
          <h1 className="text-2xl font-bold mb-2 text-center">Find People to Swap Skills</h1>
          <CategoryLocationFilter
            categories={categories}
            locations={locations}
            value={{ category, location }}
            onChange={v => { setCategory(v.category); setLocation(v.location); setPage(1); }}
          />
          {filterLoading && <div className="alert alert-info my-2">Loading filters...</div>}
          {filterError && <div className="alert alert-error my-2">{filterError}</div>}
          <SearchBar
            search={search}
            setSearch={setSearch}
            availability={availability}
            setAvailability={setAvailability}
            onSearch={() => { setPage(1); fetchProfiles(); }}
          />
        </div>
        <div className="mb-4">
          <h2 className="text-lg font-semibold mb-2 text-center">Public Profiles</h2>
          {loading ? (
            <div className="flex justify-center my-8">
              <span className="loading loading-spinner loading-lg text-primary"></span>
            </div>
          ) : error ? (
            <div className="alert alert-error my-4">{error}</div>
          ) : profiles.length === 0 ? (
            <div className="alert alert-warning my-4">No profiles found. Try adjusting your filters.</div>
          ) : (
            <div className="flex flex-col gap-4">
              {profiles.map(user => (
                <ProfileCard key={user.id} user={user} onRequestSwap={() => { setSelectedUser(user); setSwapModalOpen(true); }} />
              ))}
            </div>
          )}
        </div>
        <Pagination page={page} totalPages={totalPages} onPageChange={setPage} />
      </div>
      {/* Modal overlay for better iOS/mobile experience */}
      <div className={swapModalOpen ? "fixed inset-0 z-40 bg-black bg-opacity-40 flex items-center justify-center" : "hidden"}>
        <SwapRequestModal
          open={swapModalOpen}
          onClose={() => setSwapModalOpen(false)}
          receiver={selectedUser}
          onSuccess={() => { setSwapModalOpen(false); }}
        />
      </div>
    </div>
  );
};

export default ProfileList;
