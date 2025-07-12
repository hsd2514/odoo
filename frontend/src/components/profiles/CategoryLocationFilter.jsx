import React from "react";

/**
 * CategoryLocationFilter.jsx
 * DaisyUI + Tailwind filter bar for skill category and location.
 * For beginners: Use this in ProfileList or SearchBar for filtering.
 */
export default function CategoryLocationFilter({ categories, locations, value, onChange }) {
  return (
    <div className="flex gap-2 mb-2">
      <select
        className="select select-bordered"
        name="category"
        value={value.category || ""}
        onChange={e => onChange({ ...value, category: e.target.value })}
      >
        <option value="">All Categories</option>
        {categories.map(cat => <option key={cat} value={cat}>{cat}</option>)}
      </select>
      <select
        className="select select-bordered"
        name="location"
        value={value.location || ""}
        onChange={e => onChange({ ...value, location: e.target.value })}
      >
        <option value="">All Locations</option>
        {locations.map(loc => <option key={loc} value={loc}>{loc}</option>)}
      </select>
    </div>
  );
}
