from sqlalchemy import Column, Integer,String,DateTime,Text
from src.utils.db import Base

class Rooms(Base):
    __tablename__ = 'rooms'

    id = Column(Integer,primary_key=True,index=True)
    name = Column(String)
    created_by = Column(Integer)
    created_at = Column(DateTime)

class RoomMember(Base):
    __tablename__ = "room_member"

    id = Column(Integer,primary_key=True)
    room_id = Column(Integer)
    user_id = Column(Integer)

    