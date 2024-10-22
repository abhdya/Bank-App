from fastapi import FastAPI, Depends, status, HTTPException
from sqlalchemy.orm import Session
from . import schemas, models
from .database import engine, SessionLocal
from .hashing import Hash
from .routers import user, employee, transaction, authentication, verify, login

app = FastAPI(debug=True)  # Enable debugging for more detailed error messages

# Create all tables in the database
models.Base.metadata.create_all(engine)

    
app.include_router(authentication.router)
app.include_router(user.router)
app.include_router(employee.router)
app.include_router(transaction.router)
app.include_router(verify.router)
app.include_router(login.router)