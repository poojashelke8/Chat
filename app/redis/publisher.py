from app.redis.client import redis_client

def publish_message(message:str):
    redis_client.publish(
        "chat_room",
        message
    )