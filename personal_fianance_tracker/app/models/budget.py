# app/models/budget.py
from datetime import datetime
from typing import Optional

from sqlmodel import Field, SQLModel

from .transaction import TransactionCategory # Reusing the category enum


class Budget(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    category: TransactionCategory # Budget for a specific category
    amount: int # Budgeted amount for the period
    start_date: datetime
    end_date: datetime
    user_id: Optional[int] = Field(default=None)
