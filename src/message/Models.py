from sqlalchemy import Column, Integer, ForeignKey,String, Text, DateTime
from sqlalchemy.sql import func
from src.utils.db import Base

class Message(Base):
    __tablename__ = "messages"

    id = Column(Integer, primary_key=True)
    sender_id = Column(Integer)
    receiver_id = Column(Integer, nullable=True)
    room_id = Column(Integer, nullable=True)
    content = Column(Text)
    created_at = Column(DateTime, server_default=func.now())

class Rooms(Base):
    __tablename__ = "rooms"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    created_by = Column(Integer)
    created_at = Column(DateTime, server_default=func.now())

class RoomMember(Base):
    __tablename__ = "room_members"

    id = Column(Integer,primary_key=True)
    room_id = Column(Integer, ForeignKey("rooms.id"))
    user_id = Column(Integer, ForeignKey("users.id"))