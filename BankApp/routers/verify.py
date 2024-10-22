from fastapi import APIRouter
from fastapi.responses import HTMLResponse
from .. import database
from ..templates import s, SALT

router = APIRouter(
    prefix='/bank/verify',
    tags=["Verification"]
)

@router.get("/{token}", response_class=HTMLResponse)
async def verify_email(token: str):
    """Verify the user by decoding the token"""
    try:
        # Decode the token (within 1 hour expiry)
        email = s.loads(token, salt=SALT, max_age=3600)
       
        # Find the user in the database
        user = database.get_db.get(email)
        if user and not user["is_verified"]:
            user["is_verified"] = True
            return f"<h1>Email {email} has been successfully verified!</h1>"
        else:
            return f"<h1>Email already verified or invalid token</h1>"

    except Exception as e:
        return f"<h1>Invalid or expired token</h1>"