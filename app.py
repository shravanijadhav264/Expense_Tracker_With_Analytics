import streamlit as st
from datetime import date
from database import (
    create_tables,
    add_transaction,
    get_total_by_type,
    get_category_wise_expense,
    get_monthly_expense,
    get_transactions,
    delete_transaction
)
import pandas as pd
from analytics import plot_category_expenses, plot_monthly_expenses
import sqlite3

# ---------------- Setup ----------------
create_tables()
st.set_page_config(page_title="Expense Tracker", layout="wide")
st.title("💰 Expense Tracker with Analytics")

# ---------------- Add Transaction ----------------
st.header("Add Transaction")
with st.form("transaction_form"):
    amount = st.number_input("Amount", min_value=0.0, step=1.0)
    category = st.text_input("Category")
    txn_type = st.selectbox("Type", ["expense", "income"])
    description = st.text_input("Description")
    txn_date = st.date_input("Date", value=date.today())
    submitted = st.form_submit_button("Add")

    if submitted:
        if amount > 0 and category:
            add_transaction(amount, category, txn_type, description, str(txn_date))
            st.success("Transaction added successfully!")
        else:
            st.error("Amount and category are required.")

# ---------------- Analytics ----------------
st.header("Analytics")
col1, col2 = st.columns(2)

with col1:
    st.metric("Total Income", f"₹ {get_total_by_type('income')}")
with col2:
    st.metric("Total Expense", f"₹ {get_total_by_type('expense')}")

st.subheader("Category-wise Expense")
category_data = get_category_wise_expense()
if category_data:
    for category, total in category_data:
        st.write(f"{category} : ₹ {total}")
else:
    st.write("No expense data.")

st.subheader("Monthly Expense")
monthly_data = get_monthly_expense()
if monthly_data:
    for month, total in monthly_data:
        st.write(f"{month} : ₹ {total}")
else:
    st.write("No monthly data.")

# ---------------- Transaction Table ----------------
st.header("All Transactions")
transactions = get_transactions()
if transactions:
    df = pd.DataFrame(transactions, columns=["ID", "Amount", "Category", "Type", "Description", "Date"])
    for i, row in df.iterrows():
        cols = st.columns([1,2,2,2,3,2,1])
        cols[0].write(row["ID"])
        cols[1].write(row["Amount"])
        cols[2].write(row["Category"])
        cols[3].write(row["Type"])
        cols[4].write(row["Description"])
        cols[5].write(row["Date"])
        if cols[6].button("Delete", key=f"del_{row['ID']}"):
            delete_transaction(row["ID"])
            st.experimental_rerun()
else:
    st.write("No transactions yet.")

# ---------------- Charts ----------------
st.header("Visual Analytics")
conn = sqlite3.connect("expenses.db")
df_chart = pd.read_sql_query("SELECT * FROM transactions WHERE type='expense'", conn)
conn.close()

chart_col1, chart_col2 = st.columns(2)
with chart_col1:
    st.pyplot(plot_category_expenses(df_chart))
with chart_col2:
    st.pyplot(plot_monthly_expenses(df_chart))
