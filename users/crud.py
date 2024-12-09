from sqlalchemy.orm import Session
from users.models import User
from users.schemas import UserCreate, UserLogin

def create_user(db: Session, user: UserCreate):
    new_user = User(
        name=user.name,
        email=user.email,
        phone_no=user.phone_no,
        address=user.address,
        password=user.password  
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

def authenticate_user(db: Session, login_data: UserLogin):
    user = db.query(User).filter(User.email == login_data.email).first()
    if user and user.password == login_data.password:  
        return user
    return None
