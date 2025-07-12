# main.py — FastAPI entry point

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import auth, users, skills, swaps, feedback, badges, invites, admin

app = FastAPI()

# Enable CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register all routers (modular endpoints)
app.include_router(auth.router)
app.include_router(users.router)
app.include_router(skills.router)
app.include_router(swaps.router)
app.include_router(feedback.router)
app.include_router(badges.router)
app.include_router(invites.router)
app.include_router(admin.router)

# Root endpoint for health check
@app.get("/")
def read_root():
    return {"message": "Skill Swap API is running!"}
