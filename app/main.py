from fastapi import FastAPI,WebSocket,WebSocketDisconnect
from fastapi.responses import HTMLResponse
from redis import Redis
import json
from app.websocket.manager import ConnectionManager
from app.pubsub import start_pubsub

app = FastAPI()

# creating a redis client
redis_client = Redis(
    host="localhost",
    port=6379,
    decode_responses=True
    )

manager = ConnectionManager()


start_pubsub(redis_client,manager)


@app.post("/task")
def create_task():
    task = {
        "id":1,
        "message":"Send email"
    }

    redis_client.lpush(
        "task_queue",
        json.dumps(task)
    )

    return {"status":"Queued!"}


@app.post("/delete_task")
def delete_task():
    task = redis_client.rpop("task_queue")
    return {
        "status": "Task Popped!",
        "task": task
    }


html = """
<!DOCTYPE html>
<html>
    <head>
        <title>FastAPI WebSocket Test</title>
    </head>
    <body>
        <h1>WebSocket Test Client</h1>
        <div id="messages"></div>
        <input type="text" id="messageText" placeholder="Type a message...">
        <button onclick="sendMessage()">Send</button>
        <script>
        const username = prompt("Enter username");

const ws = new WebSocket(
    `ws://127.0.0.1:8002/ws/${username}`
);
            
ws.onopen = function () {
    console.log("WebSocket connected");
};

ws.onerror = function (err) {
    console.log("WebSocket error:", err);
};

ws.onclose = function () {
    console.log("WebSocket closed");
};

ws.onmessage = function(event) {
    var messages = document.getElementById('messages');
    var message = document.createElement('div');
    message.textContent = event.data;
    messages.appendChild(message);
};

function sendMessage() {

    const input = document.getElementById("messageText");

    ws.send(input.value);

    input.value = "";
}
        </script>
    </body>
</html>
"""
print("MAIN FILE LOADED")

@app.get("/")
async def home():
    
    return HTMLResponse(html)

@app.websocket("/ws/{username}")
async def websocket_endpoint(websocket: WebSocket,username:str):

    await manager.connect(websocket,username)

    try:
        await manager.broadcast(f"{username} joined chat")

        while True:

            data = await websocket.receive_text()
            redis_client.publish(
                "chat_room",
                f"{username} : {data}"
            )

            # await manager.broadcast(f"{username}: {data}")

    except WebSocketDisconnect:

        manager.disconnect(websocket)

        await manager.broadcast(f"{username} left chat")
    