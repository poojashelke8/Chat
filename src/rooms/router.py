from fastapi import Depends,HTTPException,APIRouter
from sqlalchemy.orm import Session
from src.rooms.Schema import RoomCreate,MemberAdd
from src.utils.db import get_db
from src.message.Models import Rooms_Msg,RoomMember_Msg




room_router = APIRouter(
    prefix="/room",
    tags=["Rooms"]
)

@room_router.post("/create_room")
def create_room(room_data:RoomCreate,db:Session=Depends(get_db)):
    new_room = Rooms_Msg(name = room_data.room_name,created_by = room_data.created_by)

    db.add(new_room)
    db.commit()
    db.refresh(new_room)
    return new_room

@room_router.post("/add_member")
def add_member(room_id:int,member:MemberAdd,db:Session=Depends(get_db)):
    room = db.query(Rooms_Msg).filter(Rooms_Msg.id == room_id).first()

    if not room:
        return HTTPException(status_code=404, detail="Room not found")

    room_member = RoomMember_Msg(room_id=room_id,user_id = member.user_id)

    db.add(room_member)
    db.commit()
    db.refresh(room_member)

    return {
        "message": "Member added successfully",
        "details":room_member
        }

@room_router.get("/all_members")
def get_members(db:Session=Depends(get_db)):
    members = db.query(RoomMember_Msg).all()

    return members

@room_router.get("/{room_id}/members")
def get_members(
    room_id: int,
    db: Session = Depends(get_db)
):
    members = (
        db.query(RoomMember_Msg)
        .filter(RoomMember_Msg.room_id == room_id)
        .all()
    )

    return members