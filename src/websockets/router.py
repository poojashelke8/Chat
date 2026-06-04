from fastapi import APIRouter, WebSocket, WebSocketDisconnect
import json
socket_router = APIRouter()

active_connections = {}

@socket_router.websocket("/ws/{user_id}")
async def websocket_endpoint(websocket: WebSocket, user_id: int):
    await websocket.accept()

    active_connections[user_id] = websocket

    try:
        while True:
            data = await websocket.receive_text()

            payload = json.loads(data)

            receiver_id = payload["receiver_id"]
            message = payload["message"]

            receiver_socket = active_connections.get(receiver_id)

            if receiver_socket:
                await receiver_socket.send_text(
                    f"User {user_id}: {message}"
                )
            print(active_connections,"active users")
            print(f"User {user_id}: {message}")

    except WebSocketDisconnect:
        active_connections.pop(user_id, None)
        print(f"User {user_id} disconnected") 