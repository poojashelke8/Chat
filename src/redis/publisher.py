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