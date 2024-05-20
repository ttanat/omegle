from fastapi import WebSocket


class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = set()

    async def connect(self, websocket: WebSocket):
        # Connect user
        await websocket.accept()
        # Add user to active_connections
        self.active_connections.add(websocket)

    def disconnect(self, user: WebSocket):
        # Remove user from active_connections
        self.active_connections.remove(user)

    async def update_num_online(self, user: WebSocket):
        await user.send_json({"action": "update_num_online", "num_online": len(self.active_connections)})
