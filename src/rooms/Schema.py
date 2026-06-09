from pydantic import BaseModel

class RoomCreate(BaseModel):
    room_name: str
    created_by :int

class MemberAdd(BaseModel):
    user_id : int