# streamlit_app.py
import streamlit as st
import pandas as pd
from datetime import datetime
from sqlmodel import Session, select
from app.database.engine import create_db_and_tables, get_session
from app.models.transaction import Transaction, TransactionType, TransactionCategory

# Ensure database and tables are created
create_db_and_tables()

st.set_page_config(layout="wide", page_title="FinTrack Pro Dashboard")
st.title("FinTrack Pro Dashboard")

# Function to get all transactions
def get_transactions(session: Session):
    return session.exec(select(Transaction)).all()

# Function to add a transaction
def add_transaction_to_db(transaction: Transaction):
    with get_session() as session:
        session.add(transaction)
        session.commit()
        session.refresh(transaction)
    st.success("Transaction added successfully!")

# --- Input Form ---
st.header("Add New Transaction")
with st.form("new_transaction_form", clear_on_submit=True):
    col1, col2 = st.columns(2)
    with col1:
        description = st.text_input("Description")
        amount = st.number_input("Amount", min_value=1, step=1, value=1)
        transaction_type = st.radio("Type", [e.value for e in TransactionType])
    with col2:
        category = st.selectbox("Category", [e.value for e in TransactionCategory])
        date = st.date_input("Date", datetime.now())
    
    submitted = st.form_submit_button("Add Transaction")
    if submitted:
        if description and amount and category and transaction_type and date:
            new_transaction = Transaction(
                description=description,
                amount=int(amount),
                category=TransactionCategory(category),
                transaction_type=TransactionType(transaction_type),
                date=datetime.combine(date, datetime.min.time()) # Convert date to datetime
            )
            add_transaction_to_db(new_transaction)
            st.rerun() # Rerun to update dashboard

# --- Dashboard Display ---
st.header("Financial Overview")

with get_session() as session_instance:
    transactions = get_transactions(session_instance)

# Convert transactions to DataFrame
transactions_data = [t.model_dump() for t in transactions]
df = pd.DataFrame(transactions_data)

if not df.empty:
    df["date"] = pd.to_datetime(df["date"])

    # Monthly Summary
    st.subheader("Monthly Summary")
    current_month = datetime.now().month
    current_year = datetime.now().year
    monthly_df = df[(df["date"].dt.month == current_month) & (df["date"].dt.year == current_year)]

    total_income = monthly_df[monthly_df["transaction_type"] == TransactionType.INCOME.value]["amount"].sum()
    total_expense = monthly_df[monthly_df["transaction_type"] == TransactionType.EXPENSE.value]["amount"].sum()
    net_flow = total_income - total_expense

    col_income, col_expense, col_net = st.columns(3)
    col_income.metric("Total Income", f"${total_income:,}")
    col_expense.metric("Total Expense", f"${total_expense:,}")
    col_net.metric("Net Flow", f"${net_flow:,}")

    # Transaction Table
    st.subheader("All Transactions")
    st.dataframe(df.sort_values(by="date", ascending=False).drop(columns=["user_id"]), use_container_width=True)

    # Expense Breakdown Chart
    st.subheader("Expense Breakdown by Category")
    expense_df = df[df["transaction_type"] == TransactionType.EXPENSE.value]
    if not expense_df.empty:
        expense_by_category = expense_df.groupby("category")["amount"].sum().sort_values(ascending=False)
        st.bar_chart(expense_by_category)
    else:
        st.info("No expenses recorded to display breakdown chart.")
else:
    st.info("No transactions recorded yet. Add some using the form above!")

