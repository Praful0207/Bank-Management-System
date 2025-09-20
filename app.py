# app.py
import streamlit as st
from bank import Bank

# Load existing data
Bank.load_data()
bank = Bank()

st.title("🏦 Simple Bank Management System")

menu = st.sidebar.selectbox("Choose Operation", [
    "Create Account",
    "Deposit",
    "Withdraw",
    "Show Details",
    "Update Account",
    "Delete Account"
])

if menu == "Create Account":
    st.subheader("Create a New Account")
    name = st.text_input("Enter Name")
    age = st.number_input("Enter Age", min_value=0, step=1)
    email = st.text_input("Enter Email")
    pin = st.text_input("Set a 4-digit PIN", type="password")

    if st.button("Create"):
        if name and email and pin.isdigit():
            result = bank.createaccount(name, int(age), email, int(pin))
            if isinstance(result, dict):
                st.success("Account Created!")
                st.json(result)
            else:
                st.error(result)
        else:
            st.warning("Please fill all fields correctly.")

elif menu == "Deposit":
    st.subheader("Deposit Money")
    acc_no = st.text_input("Account Number")
    pin = st.text_input("PIN", type="password")
    amount = st.number_input("Amount to Deposit", min_value=0)

    if st.button("Deposit"):
        if acc_no and pin and amount:
            result = bank.deposit(acc_no, int(pin), int(amount))
            st.success(result)

elif menu == "Withdraw":
    st.subheader("Withdraw Money")
    acc_no = st.text_input("Account Number")
    pin = st.text_input("PIN", type="password")
    amount = st.number_input("Amount to Withdraw", min_value=0)

    if st.button("Withdraw"):
        if acc_no and pin and amount:
            result = bank.withdraw(acc_no, int(pin), int(amount))
            st.success(result)

elif menu == "Show Details":
    st.subheader("Account Details")
    acc_no = st.text_input("Account Number")
    pin = st.text_input("PIN", type="password")

    if st.button("Show"):
        user = bank.show_details(acc_no, int(pin))
        if user:
            st.json(user)
        else:
            st.error("Invalid account number or PIN")

elif menu == "Update Account":
    st.subheader("Update Account Info")
    acc_no = st.text_input("Account Number")
    pin = st.text_input("PIN", type="password")
    name = st.text_input("New Name (optional)")
    email = st.text_input("New Email (optional)")
    new_pin = st.text_input("New PIN (optional)")

    if st.button("Update"):
        result = bank.update_user(
            acc_no,
            int(pin),
            name=name or None,
            email=email or None,
            new_pin=int(new_pin) if new_pin.isdigit() else None
        )
        st.success(result)

elif menu == "Delete Account":
    st.subheader("Delete Account")
    acc_no = st.text_input("Account Number")
    pin = st.text_input("PIN", type="password")

    if st.button("Delete"):
        result = bank.delete_account(acc_no, int(pin))
        st.warning(result)
