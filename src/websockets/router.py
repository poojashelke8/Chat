from fastapi import APIRouter, WebSocket, WebSocketDisconnect,Depends
from sqlalchemy.orm import Session
from src.utils.db import get_db,SessionLocal
import json
import asyncio
from src.message.Models import Message
from src.redis.subscriber import subscribe_to_user
from src.redis.publisher import publish_message,publish_room_message
from src.message.Models import Message,RoomMember


socket_router = APIRouter()

active_connections = {}

@socket_router.websocket("/ws/{user_id}")
async def websocket_endpoint(websocket: WebSocket, user_id: int):
    db = SessionLocal()
    await websocket.accept()

    subscriber_task = asyncio.create_task(
        subscribe_to_user(
            user_id,
            websocket,
            db
        )
    )

    active_connections[user_id] = websocket

    try:
        while True:
            data = await websocket.receive_text()

            payload = json.loads(data)

            # receiver_id = payload["receiver_id"]
            message_type = payload["type"]
            message = payload["content"]
            if message_type == "direct":
                receiver_id = payload["receiver_id"]

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
            elif message_type == "room":
                room_id = payload["room_id"]
                room_member = (
                    db.query(RoomMember).filter(
                        RoomMember.room_id == room_id,
                        RoomMember.user_id == user_id
                    )
                    .first()
                )

                if not room_member:
                    await websocket.send_json({
                        "error":"You are not a member of this room"
                    })
                    continue

                db_message = Message(
                    sender_id=user_id,
                    room_id=room_id,
                    content=message
                )

                db.add(db_message)
                db.commit()
                db.refresh(db_message)

                print("Room message saved")

                await publish_room_message(
                    room_id = room_id,
                    sender_id = user_id,
                    message = message
                )


    except WebSocketDisconnect:
        active_connections.pop(user_id, None)
        print(f"User {user_id} disconnected") 