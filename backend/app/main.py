# main.py — FastAPI entry point
from typing import List, Dict
from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Depends
from fastapi.middleware.cors import CORSMiddleware
from app.routers import auth, users, skills, swaps, feedback, badges, invites, admin
import asyncio
from app.ws.connection import manager
from app.utils.jwt import get_current_user_jwt

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

# --- Global Chat Room (in-memory, demo) ---
global_chat_connections: List[WebSocket] = []
global_chat_history: List[dict] = []

# WebSocket: /ws/global-chat?token=JWT
@app.websocket("/ws/global-chat")
async def global_chat_ws(websocket: WebSocket, token: str = None):
    user = None
    if token:
        try:
            user = get_current_user_jwt(token)
        except Exception:
            await websocket.close()
            return
    if not user:
        await websocket.close()
        return
    global_chat_connections.append(websocket)
    # Send chat history
    await websocket.send_json({"type": "history", "messages": global_chat_history})
    try:
        while True:
            data = await websocket.receive_json()
            msg = {
                "from": user.id,
                "message": data.get("message", ""),
                "timestamp": asyncio.get_event_loop().time()
            }
    except WebSocketDisconnect:
        pass

# Root endpoint for health check
@app.get("/")
def read_root():
    return {"message": "Skill Swap API is running!"}



