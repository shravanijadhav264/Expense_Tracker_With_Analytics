import streamlit as st
import pandas as pd
import sqlite3
from datetime import date

from database import (
    create_tables,
    add_transaction,
    get_total_by_type,
    get_category_wise_expense
)

from analytics import (
    plot_category_expenses,
    plot_monthly_expenses
)

# ------------------ PAGE CONFIG ------------------
st.set_page_config(
    page_title="Expense Tracker",
    layout="wide"
)

st.title("💰 Expense Tracker with Analytics")

# ------------------ DB INIT ------------------
create_tables()

# ------------------ ADD TRANSACTION ------------------
st.header("Add Transaction")

with st.form("transaction_form"):
    amount = st.number_input("Amount", min_value=0.0, step=1.0)
    category = st.text_input("Category")
    txn_type = st.selectbox("Type", ["expense", "income"])
    description = st.text_input("Description")
    txn_date = st.date_input("Date", value=date.today())

    submitted = st.form_submit_button("Add Transaction")

    if submitted:
        if amount > 0 and category.strip():
            add_transaction(
                amount,
                category,
                txn_type,
                description,
                str(txn_date)
            )
            st.success("Transaction added successfully!")
        else:
            st.error("Amount and category are required.")

# ------------------ OVERVIEW ------------------
st.header("Overview")

c1, c2 = st.columns(2)

with c1:
    st.metric("💵 Total Income", f"₹ {get_total_by_type('income')}")

with c2:
    st.metric("💸 Total Expense", f"₹ {get_total_by_type('expense')}")

# ------------------ CATEGORY BREAKDOWN (TEXT) ------------------
st.subheader("📂 Expense Breakdown by Category")

category_data = get_category_wise_expense()

if category_data:
    for category, total in category_data:
        st.write(f"**{category}** : ₹ {total}")
else:
    st.info("No expense data available.")

# ------------------ LOAD DATA FOR CHARTS ------------------
conn = sqlite3.connect("expenses.db")
df = pd.read_sql_query(
    "SELECT category, amount, date FROM transactions WHERE type='expense'",
    conn
)

# ------------------ ANALYTICS CHARTS ------------------
st.header("📊 Visual Analytics")

if df.empty:
    st.warning("No data available for charts.")
else:
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Category-wise Expenses")
        fig1 = plot_category_expenses(df)
        fig1.set_size_inches(5, 4)   # SAME SIZE
        st.pyplot(fig1)

    with col2:
        st.subheader("Monthly Expense Trend")
        fig2 = plot_monthly_expenses(df)
        fig2.set_size_inches(5, 4)   # SAME SIZE
        st.pyplot(fig2)
