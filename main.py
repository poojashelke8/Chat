from fastapi import FastAPI

from src.utils.db import Base, engine
from src.users.router import user_router
from src.websockets.router import socket_router
from src.rooms.router import room_router
app = FastAPI()

Base.metadata.create_all(bind=engine)

app.include_router(user_router)
app.include_router(socket_router)
app.include_router(room_router)


@app.get("/test")
def test():
    return {"message": "working"}