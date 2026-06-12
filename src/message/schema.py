from pydantic import BaseModel

class DirectMsg(BaseModel):
    type: str
    receiver_id :int
    content:str

class RoomMsg(BaseModel):
    type: str
    room_id :int
    content:str