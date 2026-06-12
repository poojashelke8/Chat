from src.redis.client import redis_client
import json

async def publish_message(receiver_id,
    sender_id,
    message
    ):
    print("publishing messages")
    await redis_client.publish(
       f"user_{receiver_id}",
        json.dumps({
            "sender_id":sender_id,
            "receiver_id":receiver_id,
            "message":message
        })
    )

async def publish_room_message(
        room_id,
        sender_id,
        message
):
    print(f"Publishing to room_{room_id}")
    await redis_client.publish(
        f"room_{room_id}",
        json.dumps({
            "type": "room",
            "room_id": room_id,
            "sender_id": sender_id,
            "message": message
        })
    )