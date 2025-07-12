# FastAPI + React + Tailwind + DaisyUI Monorepo

## Structure
- `backend/` — FastAPI app (Python)
- `frontend/` — React app (Vite, Tailwind CSS, DaisyUI)

## Getting Started

### Backend
```sh
cd backend
python -m venv venv
venv\Scripts\activate  # On Windows
pip install -r requirements.txt
uvicorn main:app --reload
```

### Frontend
```sh
cd frontend
npm install
npm run dev
```

## Development
- Run backend and frontend separately for local development.
- Update each app in its own folder.

---

This monorepo is ready for hackathon rapid development!
