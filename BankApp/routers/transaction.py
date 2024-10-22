from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from .. import database, models, schemas

router = APIRouter(
    prefix='/bank/transactions',
    tags=["Transactions"]
)

@router.put('/{sender_id}/{receiver_id}')
async def transaction(sender_id: int, receiver_id: int, request: schemas.TransactionCreate, db: Session = Depends(database.get_db)):
    # Fetch the sender and receiver
    sender = db.query(models.User).filter(models.User.id == sender_id).first()
    receiver = db.query(models.User).filter(models.User.id == receiver_id).first()

    # Check if sender and receiver exist
    if not sender:
        raise HTTPException(status_code=404, detail=f"Sender with id {sender_id} not found")
    if not receiver:
        raise HTTPException(status_code=404, detail=f"Receiver with id {receiver_id} not found")
    
    # Check if sender has enough balance for the transaction
    if sender.balance < request.amount:
        raise HTTPException(status_code=400, detail="Insufficient balance")

    # Perform the transaction
    sender.balance -= request.amount
    receiver.balance += request.amount

    # Create the transaction record
    db_transaction = models.Transaction(
        sender_id=sender_id,
        receiver_id=receiver_id,
        amount=request.amount
    )
    db.add(db_transaction)
    db.commit()

    # Refresh to update the sender and receiver
    db.refresh(sender)
    db.refresh(receiver)

    return {"message": "Transaction successful", "transaction": db_transaction}