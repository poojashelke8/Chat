from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.utils.db import Base, engine
from src.users.router import user_router
from src.websockets.router import socket_router
from src.rooms.router import room_router
from src.message.router import msg_router
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # or specify ["http://localhost:3000"] for frontend
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

Base.metadata.create_all(bind=engine)

app.include_router(user_router)
app.include_router(socket_router)
app.include_router(room_router)
app.include_router(msg_router)


@app.get("/test")
def test():
    return {"message": "working"}