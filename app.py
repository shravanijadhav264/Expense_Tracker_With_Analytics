import streamlit as st
from datetime import date
from database import (
    create_tables,
    add_transaction,
    get_total_by_type,
    get_category_wise_expense,
    get_monthly_expense
)

create_tables()

st.set_page_config(page_title="Expense Tracker", layout="centered")
st.title("💰 Expense Tracker with Analytics")

# ------------------ ADD TRANSACTION ------------------
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

# ------------------ ANALYTICS ------------------
st.header("Analytics")

total_income = get_total_by_type("income")
total_expense = get_total_by_type("expense")

st.metric("Total Income", f"₹ {total_income}")
st.metric("Total Expense", f"₹ {total_expense}")

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
