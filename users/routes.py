from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from users.schemas import UserCreate, UserLogin, UserResponse
from users.crud import create_user, authenticate_user
from users.models import User

router = APIRouter()

@router.post("/register", response_model=UserResponse)
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.email == user.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return create_user(db=db, user=user)

@router.post("/login", response_model=UserResponse)
def login_user(login_data: UserLogin, db: Session = Depends(get_db)):
    user = authenticate_user(db=db, login_data=login_data)
    if not user:
        raise HTTPException(status_code=400, detail="Invalid email or password")
    return user
