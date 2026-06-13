from fastapi import Depends,HTTPException,APIRouter
from sqlalchemy.orm import Session
from src.users.schema import UserCreate,UserResponse
from src.utils.db import get_db
from src.users.Models import User




user_router = APIRouter(
    prefix="/users",
    tags=["Users"]
)

@user_router.get("/")
def get_users():
    return {"message": "Users endpoint working"}

@user_router.post("/create_user",response_model=UserResponse)
def create_user(user_data:UserCreate,db:Session = Depends(get_db)):
    new_user = User(username=user_data.username)

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user

@user_router.get("/all_users")
def get_members(db:Session=Depends(get_db)):
    users = db.query(User).all()

    return users