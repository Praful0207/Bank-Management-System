# bank.py
import json
import random
import string
from pathlib import Path

class Bank:
    database = 'data.json'
    data = []

    @classmethod
    def load_data(cls):
        if Path(cls.database).exists():
            with open(cls.database) as fs:
                cls.data = json.load(fs)
        else:
            cls.data = []

    @classmethod
    def __update(cls):
        with open(cls.database, 'w') as fs:
            json.dump(cls.data, fs, indent=4)

    @classmethod
    def __accountgenerate(cls):
        id_parts = random.choices(string.ascii_letters, k=3) + \
                   random.choices(string.digits, k=3) + \
                   random.choices("!@#$%^&*", k=1)
        random.shuffle(id_parts)
        return ''.join(id_parts)

    def createaccount(self, name, age, email, pin):
        if age < 18 or len(str(pin)) != 4:
            return "Sorry, you cannot create an account (Age < 18 or Invalid PIN)"

        info = {
            "name": name,
            "age": age,
            "email": email,
            "pin": pin,
            "accountNo.": self.__accountgenerate(),
            "balance": 0
        }

        Bank.data.append(info)
        self.__update()
        return info

    def deposit(self, acc_no, pin, amount):
        user = self.find_user(acc_no, pin)
        if not user:
            return "Invalid account number or PIN"
        if amount <= 0 or amount > 100000:
            return "Amount must be between ₹1 and ₹100,000"

        user['balance'] += amount
        self.__update()
        return f"₹{amount} deposited successfully."

    def withdraw(self, acc_no, pin, amount):
        user = self.find_user(acc_no, pin)
        if not user:
            return "Invalid account number or PIN"
        if user['balance'] < amount:
            return "Insufficient balance"

        user['balance'] -= amount
        self.__update()
        return f"₹{amount} withdrawn successfully."

    def find_user(self, acc_no, pin):
        return next((u for u in Bank.data if u['accountNo.'] == acc_no and u['pin'] == pin), None)

    def show_details(self, acc_no, pin):
        user = self.find_user(acc_no, pin)
        return user

    def update_user(self, acc_no, pin, name=None, email=None, new_pin=None):
        user = self.find_user(acc_no, pin)
        if not user:
            return "Invalid account number or PIN"

        if name:
            user['name'] = name
        if email:
            user['email'] = email
        if new_pin:
            user['pin'] = new_pin

        self.__update()
        return "Details updated successfully."

    def delete_account(self, acc_no, pin):
        user = self.find_user(acc_no, pin)
        if not user:
            return "Invalid account number or PIN"
        Bank.data.remove(user)
        self.__update()
        return "Account deleted successfully."
