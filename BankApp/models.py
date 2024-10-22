# models.py
from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from .database import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, index=True)
    password = Column(String(100))
    balance = Column(Float, default=0.0)
    emp_id = Column(Integer, ForeignKey('employees.id'))  # Correct usage
    employee = relationship("Employee", back_populates="users")

    # Define the relationship for transactions sent by the user
    sent_transactions = relationship("Transaction", foreign_keys='Transaction.sender_id', back_populates="sender")
    # Optionally define received transactions if needed
    received_transactions = relationship("Transaction", foreign_keys='Transaction.receiver_id', back_populates="receiver")

class Transaction(Base):
    __tablename__ = "transactions"
    id = Column(Integer, primary_key=True, index=True)
    sender_id = Column(Integer, ForeignKey("users.id"))
    receiver_id = Column(Integer, ForeignKey("users.id"))
    amount = Column(Float, nullable=False)

    sender = relationship("User", foreign_keys=[sender_id], back_populates="sent_transactions")
    receiver = relationship("User", foreign_keys=[receiver_id], back_populates="received_transactions")

class Employee(Base):
    __tablename__ = "employees"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    department_id = Column(Integer, nullable=False)
    department = Column(String(100), nullable=False)
    position = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, index=True)

    users = relationship("User", back_populates="employee")

