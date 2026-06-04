import json
from src.redis.client import redis_client

async def subscribe_to_user(user_id,websocket):
    pubsub = redis_client.pubsub()

    channel = f"user_{user_id}"

    await pubsub.subscribe(channel)

    try:
        async for message in pubsub.listen():
            if message["type"] != "message":
                continue

            data = json.loads(message['data'])

            await websocket.send_json(data)
    finally:
        await pubsub.unsubscribe(channel)
        await pubsub.close()
