from redis import Redis

redis_client = Redis(
    host="localhost",
    port=6379,
    decode_responses=True
)

print("Worker started...")

while True:
    result = redis_client.brpop("task_queue", timeout=0)
    print(result)