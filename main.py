from fastapi import FastAPI

from src.utils.db import Base, engine
from src.users.router import user_router
from src.websockets.router import socket_router

app = FastAPI()

Base.metadata.create_all(bind=engine)

app.include_router(user_router)
app.include_router(socket_router)


@app.get("/test")
def test():
    return {"message": "working"}