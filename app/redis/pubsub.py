# import threading
# from redis.asyncio import Redis

# def start_pubsub(redis_client,manager):
#     pubsub = redis_client.pubsub()
#     pubsub.subscribe("chat_room")

#     async def listener():

#         async for message in pubsub.listen():

#             if message["type"] == "message":

#                 data = message["data"]

#                 import asyncio
#                 asyncio.run(
#                     manager.broadcast(data)
#                 )

#     thread = threading.Thread(
#         target=listener,
#         daemon=True
#     )

#     thread.start()