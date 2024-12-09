from pydantic import BaseModel

class UserCreate(BaseModel):
    name: str
    email: str
    phone_no: str
    address: str
    password: str

class UserLogin(BaseModel):
    email: str
    password: str

class UserResponse(BaseModel):
    id: int
    name: str
    email: str
    phone_no: str
    address: str

    class Config:
        orm_mode = True
