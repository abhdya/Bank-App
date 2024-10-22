from pydantic import BaseModel
from typing import Union

class UserBase(BaseModel):
    name: str
    email: str
    password: str
    #is_verified: bool = False

class UserCreate(UserBase):
    pass

class UserResponse(BaseModel):
    id: int
    name: str
    balance: float
    emp_id: int

    class Config:
        from_attributes = True

class TransactionCreate(BaseModel):
    sender_id: int
    receiver_id: int
    amount: float

class EmployeeBase(BaseModel):
    name: str
    department_id: int
    department: str
    position: str
    email: str

class EmployeeResponse(EmployeeBase):
    id: int

    class Config:
        from_attributes = True
        
class Login(BaseModel):
    username: str
    password: str
    
class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: Union[str, None] = None