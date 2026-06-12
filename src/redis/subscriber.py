import json
# from fastapi import Depends
from sqlalchemy.orm import Session
from src.redis.client import redis_client
from src.message.Models import RoomMember
# from src.utils.db import get_db

async def subscribe_to_user(user_id,websocket,db:Session):
    pubsub = redis_client.pubsub()

    channel = f"user_{user_id}"

    await pubsub.subscribe(channel)
    rooms =( db.query(RoomMember).filter(RoomMember.user_id == user_id).all())

    for room in rooms:
        await pubsub.subscribe(f"room_{room.room_id}")
    try:
        async for message in pubsub.listen():
            if message["type"] != "message":
                continue

            data = json.loads(message['data'])

            await websocket.send_json(data)
    finally:
        await pubsub.unsubscribe(channel)
        await pubsub.close()
