from fastapi import APIRouter,Depends
from sqlalchemy.orm import Session
from src.utils.db import get_db
from src.message.Models import Message
from src.message.Models import Message

msg_router = APIRouter()
msg_router = APIRouter()
@msg_router.get("/{sender_id}/{receiver_id}")
def get_messages(sender_id: int, receiver_id: int, db: Session = Depends(get_db)):
    messages = (
        db.query(Message)
        .filter(
            # both directions — sent and received
            (Message.sender_id == sender_id) & (Message.receiver_id == receiver_id) |
            (Message.sender_id == receiver_id) & (Message.receiver_id == sender_id)
        )
        .order_by(Message.created_at.asc())  # oldest first
        .all()
    )

    return{
"details":
    [
        {
            "id": m.id,
            "sender_id": m.sender_id,
            "receiver_id": m.receiver_id,
            "content": m.content,
            "created_at": m.created_at
        }
        for m in messages
    ]
    }