from fastapi import FastAPI,WebSocket,WebSocketDisconnect
from fastapi.responses import HTMLResponse
from app.websocket.manager import ConnectionManager

app = FastAPI()

manager = ConnectionManager()

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

            await manager.broadcast(f"{username}: {data}")

    except WebSocketDisconnect:

        manager.disconnect(websocket)

        await manager.broadcast(f"{username} left chat")
    