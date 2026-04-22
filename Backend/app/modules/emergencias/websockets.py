from fastapi import WebSocket
from typing import List, Dict

class ConnectionManager:
    def __init__(self):
        # Para diferenciar a clientes y talleres, usaremos grupos.
        self.active_connections: List[WebSocket] = []
        self.talleres_connections: List[WebSocket] = []
        self.client_connections: Dict[int, WebSocket] = {} # user_id -> ws

    async def connect_taller(self, websocket: WebSocket):
        await websocket.accept()
        self.talleres_connections.append(websocket)

    def disconnect_taller(self, websocket: WebSocket):
        self.talleres_connections.remove(websocket)

    async def connect_client(self, websocket: WebSocket, client_id: int):
        await websocket.accept()
        self.client_connections[client_id] = websocket

    def disconnect_client(self, client_id: int):
        if client_id in self.client_connections:
            del self.client_connections[client_id]

    async def broadcast_to_talleres(self, message: dict):
        for connection in self.talleres_connections:
            await connection.send_json(message)

    async def send_to_client(self, client_id: int, message: dict):
        if client_id in self.client_connections:
            await self.client_connections[client_id].send_json(message)

manager = ConnectionManager()