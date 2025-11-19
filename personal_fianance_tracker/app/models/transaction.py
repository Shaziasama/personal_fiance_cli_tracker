# app/models/transaction.py
from datetime import datetime
from enum import Enum
from typing import Optional

from sqlmodel import Field, SQLModel


class TransactionType(str, Enum):
    INCOME = "Income"
    EXPENSE = "Expense"


class TransactionCategory(str, Enum):
    FOOD = "Food"
    TRANSPORT = "Transport"
    UTILITIES = "Utilities"
    RENT = "Rent"
    SALARY = "Salary"
    ENTERTAINMENT = "Entertainment"
    SHOPPING = "Shopping"
    HEALTHCARE = "Healthcare"
    EDUCATION = "Education"
    SAVINGS = "Savings"
    INVESTMENT = "Investment"
    OTHER = "Other" # For uncategorized transactions


class Transaction(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    description: str
    amount: int
    date: datetime = Field(default_factory=datetime.utcnow)
    category: TransactionCategory
    transaction_type: TransactionType
    user_id: Optional[int] = Field(default=None)
