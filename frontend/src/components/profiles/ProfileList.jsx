import React, { useState, useEffect } from "react";
import ProfileCard from "./ProfileCard";
import SearchBar from "./SearchBar";
import Pagination from "./Pagination";
import CategoryLocationFilter from "./CategoryLocationFilter";

/**
 * ProfileList - Displays paginated public profiles with search and filter
 */
const ProfileList = () => {
  const [profiles, setProfiles] = useState([]);
  const [search, setSearch] = useState("");
  const [availability, setAvailability] = useState("");
  const [category, setCategory] = useState("");
  const [location, setLocation] = useState("");
  const [categories, setCategories] = useState([]);
  const [locations, setLocations] = useState([]);
  const [page, setPage] = useState(1);
  const [totalPages, setTotalPages] = useState(1);
  const pageSize = 10;

  const fetchProfiles = async () => {
    const params = new URLSearchParams({
      ...(search && { search }),
      ...(availability && { availability }),
      ...(category && { category }),
      ...(location && { location }),
      page,
      page_size: pageSize,
    });
    const res = await fetch(`http://localhost:8000/users/public?${params}`);
    if (res.ok) {
      const data = await res.json();
      setProfiles(data);
      setTotalPages(5);
    }
  };

  // Fetch categories and locations for filters
  useEffect(() => {
    fetch("http://localhost:8000/skills/categories")
      .then(res => res.json())
      .then(setCategories);
    fetch("http://localhost:8000/users/locations")
      .then(res => res.json())
      .then(setLocations);
  }, []);

  useEffect(() => {
    fetchProfiles();
    // eslint-disable-next-line
  }, [search, availability, category, location, page]);

  return (
    <div className="max-w-2xl mx-auto p-4">
      <CategoryLocationFilter
        categories={categories}
        locations={locations}
        value={{ category, location }}
        onChange={v => { setCategory(v.category); setLocation(v.location); setPage(1); }}
      />
      <SearchBar
        search={search}
        setSearch={setSearch}
        availability={availability}
        setAvailability={setAvailability}
        onSearch={() => { setPage(1); fetchProfiles(); }}
      />
      {profiles.map(user => (
        <ProfileCard key={user.id} user={user} onRequest={() => alert(`Request sent to ${user.name}`)} />
      ))}
      <Pagination page={page} totalPages={totalPages} onPageChange={setPage} />
    </div>
  );
};

export default ProfileList;
