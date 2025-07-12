import React from "react";

/**
 * Pagination - DaisyUI pagination controls
 * Props: page, totalPages, onPageChange
 */
const Pagination = ({ page, totalPages, onPageChange }) => (
  <div className="flex gap-1 justify-center mt-4">
    {Array.from({ length: totalPages }, (_, i) => (
      <button
        key={i + 1}
        className={`btn btn-sm ${page === i + 1 ? "btn-primary" : "btn-ghost"}`}
        onClick={() => onPageChange(i + 1)}
      >
        {i + 1}
      </button>
    ))}
  </div>
);

export default Pagination;
