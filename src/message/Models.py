from sqlalchemy import Column, Integer, String, Text, DateTime
from sqlalchemy.sql import func
from src.utils.db import Base

class Message(Base):
    __tablename__ = "messages"

    id = Column(Integer, primary_key=True)
    sender_id = Column(String)
    receiver_id = Column(String)
    content = Column(Text)
    created_at = Column(DateTime, server_default=func.now())