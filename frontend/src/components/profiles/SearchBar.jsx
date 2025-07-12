import React from "react";

/**
 * SearchBar - DaisyUI search and filter bar for profiles
 * Props: search, setSearch, availability, setAvailability, onSearch
 */
const SearchBar = ({ search, setSearch, availability, setAvailability, onSearch }) => (
  <form className="flex gap-2 mb-4" onSubmit={e => { e.preventDefault(); onSearch(); }}>
    <input
      type="text"
      placeholder="Search by name or email"
      className="input input-bordered"
      value={search}
      onChange={e => setSearch(e.target.value)}
    />
    <select
      className="select select-bordered"
      value={availability}
      onChange={e => setAvailability(e.target.value)}
    >
      <option value="">Availability</option>
      <option value="weekends">Weekends</option>
      <option value="weekdays">Weekdays</option>
      <option value="evenings">Evenings</option>
    </select>
    <button type="submit" className="btn btn-secondary">Search</button>
  </form>
);

export default SearchBar;
