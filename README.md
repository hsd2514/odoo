# Video Demo

[![Watch the video](https://img.youtube.com/vi/SfjpJaB7JDI/maxresdefault.jpg)](https://www.youtube.com/watch?v=SfjpJaB7JDI)
[link](https://www.youtube.com/watch?v=SfjpJaB7JDI)


# Odoo Hackathon Monorepo

## About the Project

This project is a full-stack skill swap and networking platform built for hackathons. It features a modular FastAPI backend and a modern React + Tailwind CSS + DaisyUI frontend. Users can create profiles, offer/request skills, send swap/invite requests, give feedback, earn badges, and explore trending skills—all in a clean, beginner-friendly codebase.

## Features

- User registration, login, and profile management
- Offer and request skills (with categories and trending)
- Swap and invite request system (with feedback and rating)
- Badges and achievements for user activity
- Advanced filtering by location, skill, and category
- Public profile browsing and detailed profile pages
- Admin endpoints and analytics (if enabled)
- Demo data seeding for rapid testing
- JWT authentication and CORS for secure, modern dev
- Responsive, DaisyUI-powered frontend with modular React components


## Project Overview

This hackathon monorepo is a full-stack platform for skill swapping and networking, built for rapid development and easy collaboration. It combines a modular FastAPI backend with a modern React + Tailwind CSS + DaisyUI frontend.

### Key Features

#### Backend (FastAPI)
- User Management: Register, login, edit profile, public/private profiles.
- Skill System: Users can offer and request skills, with categories and trending skills.
- Swap & Invite Requests: Request swaps or invites, accept/decline, and leave feedback or ratings.
- Badges & Achievements: Earn badges for activity and display them on profiles.
- Filtering: Search and filter users by location, skill, or category.
- Admin Tools: Endpoints for admin actions and analytics.
- Demo Data Seeder: Script to quickly populate the database with users and skills for testing.
- JWT Auth: Secure endpoints with JSON Web Tokens.
- CORS: Ready for local frontend-backend development.

#### Frontend (React + Tailwind + DaisyUI)
- Modern UI: Clean, responsive design using DaisyUI and Tailwind.
- Profile List: Browse public profiles with advanced filters.
- Profile Cards: See user info, skills, and take actions (swap/invite).
- Public Profile Page: View details and request swaps/invites.
- Trending Skills Widget: See what’s popular right now.
- Badges Display: Show off earned badges.
- Authentication: Register, login, and manage user state globally.
- Error Handling: Robust error boundaries and defensive rendering.
- Admin Panel: For managing users and platform data (if enabled).

#### Dev Experience
- Monorepo: Backend and frontend in one place for easy teamwork.
- Beginner Friendly: Clear code, comments, and modular structure.
- VS Code & GitHub Ready: Includes settings and Copilot instructions for productivity.
- Easy Seeding: Populate demo data with a single command.

**Demo Users:**
- Emails: `user0@test.com` ... `user49@test.com`
- Password: `test123`

**Quick Start:**
- See the README for setup instructions for both backend and frontend.


## Features

### Backend (FastAPI)
- Modular FastAPI app with routers for users, skills, swaps, invites, feedback, badges, and admin
- PostgreSQL database with SQLAlchemy ORM
- JWT authentication (login, register, protected endpoints)
- User profile management (edit, view, public/private)
- Skill management (categories, trending, offered/wanted)
- Swap and invite request system (request, accept, feedback, rating)
- Badges and trending skills endpoints
- Location and category-based filtering
- Random demo data seeding script (`seed_data.py`)
- CORS enabled for local frontend

### Frontend (React + Tailwind + DaisyUI)
- Modern, responsive UI using DaisyUI and Tailwind utility classes
- Modular React components for profiles, filters, trending skills, badges, admin panel, etc.
- Public profile list with advanced filtering (location, category, skill)
- Profile cards with skills, rating, and action buttons
- Public user profile page with swap/invite request modals
- Auth context for login/register/logout and protected routes
- Trending skills widget and badge display
- Error boundaries and defensive rendering for robust UX

### Dev Experience
- Monorepo structure: `backend/` for FastAPI, `frontend/` for React
- `.vscode` and `.github` folders for team productivity
- Beginner-friendly code and comments throughout
- Easy seeding: `python -m app.seed_data` from `backend/` to populate demo data

## Quick Start

1. **Backend:**
   - Install dependencies: `pip install -r backend/app/requirements.txt`
   - Run dev server: `uvicorn app.main:app --reload --host 0.0.0.0 --port 8000`
   - Seed demo data: `cd backend && python -m app.seed_data`

2. **Frontend:**
   - `cd frontend`
   - Install dependencies: `npm install`
   - Start dev server: `npm run dev`

3. **Visit:**
   - Frontend: [http://localhost:5173](http://localhost:5173)
   - Backend: [http://localhost:8000/docs](http://localhost:8000/docs)

## Folder Structure

- `backend/app/` — FastAPI app (routers, models, schemas, seeders)
- `frontend/src/` — React app (components, pages, context)
- `.vscode/` — VS Code settings
- `.github/` — GitHub workflows and Copilot instructions

## Example Users
- All demo users: email `user0@test.com` ... `user49@test.com`, password: `test123`

---

For more details, see code comments and router docstrings. Happy hacking!
