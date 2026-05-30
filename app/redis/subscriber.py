from app.redis.client import redis_client

async def start_pubsub(manager):

    pubsub = redis_client.pubsub()

    await pubsub.subscribe("chat_room")

    print("Subscribed to chat_room")

    async for message in pubsub.listen():

        if message["type"] == "message":

            data = message["data"]

            print("Received:", data)

            await manager.broadcast(data)