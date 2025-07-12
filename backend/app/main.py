# main.py — FastAPI entry point
from fastapi import FastAPI
from app.routers import auth, users, skills, swaps, feedback, badges, invites, admin

app = FastAPI()

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
