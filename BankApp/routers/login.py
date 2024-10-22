from fastapi import APIRouter, HTTPException, Form
from ..database import get_db

router = APIRouter(
    prefix='/bank/login',
    tags=["LogIn"])


@router.post("/")
async def login(email: str = Form(...), password: str = Form(...)):
    """Login the user after verifying their credentials"""
    user = get_db.get(email)
   
    if user and user["password"] == password:
        if user["is_verified"]:
            return {"message": "Login successful"}
        else:
            return {"message": "Please verify your email first"}
    else:
        raise HTTPException(status_code=400, detail="Invalid credentials")