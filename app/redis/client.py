# from redis.asyncio import Redis
# from fastapi import FastAPI

# app = FastAPI()

# # creating a redis client
# redis_client = Redis(
#     host="localhost",
#     port=6379,
#     decode_responses=True
#     )


from redis.asyncio import Redis

redis_client = Redis(
    host="localhost",
    port=6379,
    decode_responses=True
)