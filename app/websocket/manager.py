from fastapi import WebSocket

class ConnectionManager:

    def __init__(self):
        self.active_connections: dict[WebSocket,str] = {}


    async def connect(self, websocket: WebSocket,username:str):

        await websocket.accept()

        self.active_connections[websocket] = username


    def disconnect(self, websocket: WebSocket):

        self.active_connections.pop(websocket,None)


    async def broadcast(self, message: str):

        for connection in self.active_connections:

            await connection.send_text(message)