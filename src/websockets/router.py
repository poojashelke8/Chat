from fastapi import APIRouter, WebSocket, WebSocketDisconnect,Depends
from sqlalchemy.orm import Session
from src.utils.db import get_db,SessionLocal
import json
import asyncio
from src.message.Models import Message
from src.redis.subscriber import subscribe_to_user
from src.redis.publisher import publish_message


socket_router = APIRouter()

active_connections = {}

@socket_router.websocket("/ws/{user_id}")
async def websocket_endpoint(websocket: WebSocket, user_id: int):
    db = SessionLocal()
    await websocket.accept()

    subscriber_task = asyncio.create_task(
        subscribe_to_user(
            user_id,
            websocket
        )
    )

    active_connections[user_id] = websocket

    try:
        while True:
            data = await websocket.receive_text()

            payload = json.loads(data)

            receiver_id = payload["receiver_id"]
            message = payload["content"]

            db_message = Message(sender_id = user_id,
                                 receiver_id = receiver_id,
                                 content = message)
            
            print(db_message,"database message")
            
            db.add(db_message)
            db.commit()
            db.refresh(db_message)

            print("Message saved")

            await publish_message(
                receiver_id=receiver_id,
                sender_id=user_id,
                message=message
            )

#             receiver_socket = active_connections.get(receiver_id)


#             if receiver_socket:
#                 await receiver_socket.send_json({
#     "sender_id": user_id,
#     "receiver_id": receiver_id,
#     "message": message
# })
            

    except WebSocketDisconnect:
        active_connections.pop(user_id, None)
        print(f"User {user_id} disconnected") 