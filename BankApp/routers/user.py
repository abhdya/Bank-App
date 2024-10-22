from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session
from .. import schemas, database, hashing, models, templates, verification
import traceback
from ..oauth2 import get_current_user
import logging

router = APIRouter(
    prefix='/bank/users',
    tags=["Users"]
)

logger = logging.getLogger("uvicorn.error")
@router.post('/', response_model=schemas.UserResponse, status_code=status.HTTP_201_CREATED)
async def create_user(request: schemas.UserBase, db: Session = Depends(database.get_db)):
    hashedPassword = hashing.Hash.hash_argon(request.password)

    # Check if the email already exists
    user_exists = db.query(models.User).filter(models.User.email == request.email).first()
    if user_exists:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered")

    try:
        employees = db.query(models.Employee).all()
        if not employees:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No employees available")
        
        total_users = db.query(models.User).count()
        assigned_emp_id = employees[total_users % len(employees)].id
        
        new_user = models.User(name=request.name, email=request.email, password=hashedPassword, emp_id=assigned_emp_id)
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        
    except Exception as e:
        # Log the full traceback
        print("An error occurred:", e)
        traceback.print_exc()  # This will give you a detailed stack trace in your logs
        raise HTTPException(status_code=500, detail=f"Error creating user: {str(e)}")
    
    return new_user

# async def create_user(request: schemas.UserBase, db: Session = Depends(database.get_db)):
#     hashedPassword =  hashing.Hash.hash_argon(request.password)

#     try:
#         employees = db.query(models.Employee).all()
#         if not employees:
#             raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No employees available")
        
#         total_users = db.query(models.User).count()
#         assigned_emp_id = employees[total_users % len(employees)].id
        
#         new_user = models.User(name=request.name, email=request.email, password=hashedPassword, emp_id=assigned_emp_id)
#         db.add(new_user)
#         db.commit()
#         db.refresh(new_user)
        
#     except Exception as e:
#         # Log the full traceback
#         print("An error occurred:", e)
#         traceback.print_exc()  # This will give you a detailed stack trace in your logs
#         raise HTTPException(status_code=500, detail=f"Error creating user: {str(e)}")
    
#     # Generate a unique token for the user
#     #token = templates.s.dumps(new_user, salt=templates.SALT)
    
#     # verification.send_verification_email(new_user, token)
   
#     # return {"message": f"Registration successful. Verification email sent to {new_user}"}

@router.get('/')
async def get_users(db: Session = Depends(database.get_db), 
                    current_user: schemas.UserBase = Depends(get_current_user)):
    try:
        users = db.query(models.User).all()
        return users
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching users: {str(e)}")
    
@router.get('/{id}', response_model=schemas.UserResponse, tags=["Users"])
async def get_users_id(id: int, db: Session = Depends(database.get_db)):
    try:
        user = db.query(models.User).filter(models.User.id == id).first()
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id = {id} not found")
        return user
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching users: {str(e)}")

@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(id: int, db: Session = Depends(database.get_db)):
    try:
        user = db.query(models.User).filter(models.User.id == id).first()
        
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id = {id} not found")
        
        db.delete(user)
        db.commit()
        
        return {"detail": "User deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error deleting user: {str(e)}")
    
@router.put('/{id}')
async def update_user_balance(id: int, amount: float, db:Session = Depends(database.get_db)):
    try:
        user = db.query(models.User).filter(models.User.id == id).first()
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id = {id} not found")
        user.balance += amount
        db.commit()
        db.refresh(user)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error updating user balance: {str(e)}")
    