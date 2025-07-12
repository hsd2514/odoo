
# 🚀 Skill Swap Platform – Backend (FastAPI)

This folder contains the FastAPI backend for the Skill Swap MVP. It is modular, beginner-friendly, and ready for hackathon development.

## 📁 Structure
- `main.py` — FastAPI entry point (registers all routers)
- `config.py` — Environment variables & settings
- `database.py` — DB engine and session
- `models/` — SQLAlchemy models (user, skill, swap, feedback, badge, invite)
- `schemas/` — Pydantic schemas for request/response
- `routers/` — FastAPI route definitions (auth, users, skills, swaps, feedback, badges, invites, admin)
- `services/` — Business logic (recommender, badge engine, websocket manager)
- `ws/` — WebSocket handlers
- `utils/` — Helpers (auth, hashing, etc.)

## 🏁 How to Run
1. `cd backend`
2. `python -m venv venv`
3. `venv\Scripts\activate` (Windows) or `source venv/bin/activate` (Mac/Linux)
4. `pip install -r requirements.txt`
5. `uvicorn app.main:app --reload`

## 📝 Key Features
- User registration/login (JWT)
- Add/remove skills (offered/wanted)
- Search users by skill/location/availability
- Skill swap requests & management
- Feedback, ratings, and badges
- Real-time swap alerts (WebSockets)
- Admin endpoints for moderation

## 🗂️ Tips for Contributors
- Always use routers (`from fastapi import APIRouter`) for endpoints.
- Write modular code and keep files as small and focused as possible.
- Use clear docstrings and type hints.
- Add comments and examples for beginners.

---
See the main project README for full feature list, API endpoints, and hackathon timeline.
