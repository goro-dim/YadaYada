from typing import List
from fastapi import WebSocket

class ChatManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket, username: str):
        await websocket.accept()
        self.active_connections.append(websocket)
        await self.broadcast(f"{username} joined the chat!")

    def disconnect(self, websocket: WebSocket, username: str):
        self.active_connections.remove(websocket)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            await connection.send_text(message)
