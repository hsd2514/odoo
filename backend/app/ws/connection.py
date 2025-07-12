# ws/connection.py
# FastAPI WebSocket manager for real-time events
from fastapi import WebSocket
from typing import Dict, List

class ConnectionManager:
    def __init__(self):
        self.active_connections: Dict[int, List[WebSocket]] = {}
        self.admin_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket, user_id: int = None, is_admin: bool = False):
        await websocket.accept()
        if is_admin:
            self.admin_connections.append(websocket)
        elif user_id is not None:
            self.active_connections.setdefault(user_id, []).append(websocket)

    def disconnect(self, websocket: WebSocket, user_id: int = None, is_admin: bool = False):
        if is_admin:
            if websocket in self.admin_connections:
                self.admin_connections.remove(websocket)
        elif user_id is not None:
            if user_id in self.active_connections and websocket in self.active_connections[user_id]:
                self.active_connections[user_id].remove(websocket)
                if not self.active_connections[user_id]:
                    del self.active_connections[user_id]

    async def send_personal_message(self, message: dict, user_id: int):
        for ws in self.active_connections.get(user_id, []):
            await ws.send_json(message)

    async def broadcast_admin(self, message: dict):
        for ws in self.admin_connections:
            await ws.send_json(message)

    async def broadcast_announcement(self, message: dict):
        # Broadcast to all users and admins
        for ws_list in self.active_connections.values():
            for ws in ws_list:
                await ws.send_json(message)
        for ws in self.admin_connections:
            await ws.send_json(message)

manager = ConnectionManager()
