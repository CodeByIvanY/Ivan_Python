import sys
import sqlite3
from tabulate import tabulate
from datetime import datetime

connection = sqlite3.connect("project.db")
cursor = connection.cursor()

is_login = False

class Account:
    def __init__(self, account=None, name='User', hashed_password=None, balance=100):
        self.account = account
        self.hashed_password = hashed_password
        self.name = name
        self.balance = balance
    def deposit(self, amount):
        if amount > 0:
            self.balance += amount
            cursor.execute("INSERT INTO tb_transactions (Account_id, TransType, Amount) VALUES (?, 'Deposit', ?);", (self.account, amount))
            connection.commit()
            return self.balance
        else:
            return f'NPAmt'

    def withdraw(self, amount):
        if amount > 0:
            if amount <= self.balance:
                self.balance -= amount
                cursor.execute("INSERT INTO tb_transactions (Account_id, TransType, Amount) VALUES (?, 'Withdraw', ?);", (self.account, -amount))
                connection.commit()
                return self.balance
            else:
                return f'NSF'
        else:
            return f'NPAmt'

def main():
    global is_login
      # Initialize account with a name
    account = Account()
    while True:
        if not is_login:
            print("----------------------")
            print("| RCL Banking System |")
            print("| 1. Login           |")
            print("| 2. Sign Up         |")
            print("| 3. Exit            |")
            print("----------------------")

            choice_Login_Page = input("Enter your choice (1-3): ")
            if choice_Login_Page == "1":
                login(account)
            elif choice_Login_Page == "2":
                sign_out(account)
            elif choice_Login_Page == "3":
                break
            else:
                print("That is not a valid choice.")
            continue

        print("----------------------")
        print("| RCL Banking System |")
        print("| 1. Show Balance    |")
        print("| 2. Deposit         |")
        print("| 3. Withdraw        |")
        print("| 4. User Info       |")
        print("| 5. Exit            |")
        print("----------------------")
        choice = input("Enter your choice (1-5): ")

        if choice == '1':
            show_balance(account.balance)
        elif choice == '2':
            deposit(account)
        elif choice == '3':
            withdraw(account)
        elif choice == '4':
            accountinfo(account)
        elif choice == '5':
            break
        else:
            print("That is not a valid choice")


    print("**************************************************************************")
    print(f"Thank you [{account.name}] for using RCL Banking System! Have a nice day!")
    print("**************************************************************************")


def login(account):
    global is_login
    print("*****************************************************************")
    AccNum = input("Enter your account number: ")
    password = input("Enter your password: ")
    # Here you would typically check against a database or a predefined list
    sql_login = cursor.execute("SELECT id FROM tb_accounts WHERE id = ? AND Password = ? LIMIT 1;", (AccNum, password)).fetchone()

    if sql_login is not None and sql_login[0] is not None:
        is_login = True
        # Update account name, balance
        sql_userName = cursor.execute("SELECT COALESCE(first_name, '') || ' ' || COALESCE(last_name, '') AS full_name FROM tb_userinfo WHERE Account_id = ? LIMIT 1;", (AccNum,),).fetchone()
        sql_balance = cursor.execute("SELECT SUM(Amount) FROM tb_transactions WHERE Account_id = ?;", (AccNum,),).fetchone()
        account.account = AccNum
        account.name = sql_userName[0] if sql_userName else "Unknown User"
        account.balance = sql_balance[0] if sql_balance and sql_balance[0] is not None else 0
        account.hashed_password = password

        print(f"Welcome {account.name}, Login successful!")
    else:
        print("Invalid credentials. Please try again.")
    print("*****************************************************************")

def sign_out(account):
    # Prompt user for input
    first_name = get_input("Enter your first name: ")
    last_name = get_input("Enter your last name: ")
    password = get_input("Enter your password (at least 8 characters): ", min_length=8)

    gender = input("Enter your Gender [M/F/Blank] - Optional: ").strip() or None
    birthday = input("Enter your Birthday [MM/DD/YYYY] - Optional: ").strip() or None
    address = input("Enter your Full Address - Optional: ").strip() or None
    contact_number = input("Enter your Contact Number [(123)456-7890] - Optional: ").strip() or None
    Full_name = f"{first_name}, {last_name}"
    # Generate a unique account number
    account_number = int(round(datetime.timestamp(datetime.now()), 0)) - 1030206040 + 7613000000000000

    # SQL queries
    query_accnum = "INSERT INTO tb_accounts (id, Password) VALUES (?, ?);"
    query_userinfo = """INSERT INTO tb_userinfo (Account_id, First_Name, Last_Name, Gender, Birthday, Address, Contact_Number)
                        VALUES (?, ?, ?, ?, ?, ?, ?);"""

    print("*****************************************************************")
    try:
        # Execute the second query to insert user information
        cursor.execute(query_userinfo, (account_number, first_name, last_name, gender, birthday, address, contact_number))
        connection.commit()

        # Execute the first query to insert account number and password
        cursor.execute(query_accnum, (account_number, password))
        connection.commit()

        print("Successfully signed out.")
        print(f"Dear User - {Full_name}. Your account number is {account_number}.")
    except sqlite3.Error as e:
        print(f"An error occurred while signing out the account: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
    print("*****************************************************************")

    account.account = account_number
    account.name = Full_name
    account.hashed_password = password
    account.balance = 0
    global is_login
    is_login = True

    return

def get_input(prompt, title_case=True, min_length=None):
    """Helper function to get user input with optional title casing and length validation."""
    while True:
        user_input = input(prompt).strip()
        if title_case:
            user_input = user_input.title()
        if min_length and len(user_input) < min_length:
            print(f"Error: Input must be at least {min_length} characters long.")
        elif not user_input:
            print("Error: This field must be provided.")
        else:
            return user_input

def show_balance(balance):
    print("*****************************************************************")
    print(f"Your balance is ${balance:.2f}")
    print("*****************************************************************")


def deposit(account):
    try:
        amount = round(float(input("Enter an amount to be deposited:")),2)
        result = account.deposit(amount)
    except ValueError:
        print("*****************************************************************")
        print(f"Only numeric amounts are allowed. Your balance is ${account.balance:.2f}")
        print("*****************************************************************")
        return

    print("*****************************************************************")
    if result == "NPAmt":
        print(f"Deposit amount must be positive.")
    else:
        print(f"Deposited ${amount:.2f}. New balance is ${result:.2f}")
    print("*****************************************************************")


def withdraw(account):
    try:
        amount = round(float(input("Enter an amount to be withdrawed:")),2)
        result = account.withdraw(amount)
    except ValueError:
        print("*****************************************************************")
        print(f"Only numeric amounts are allowed. Your balance is ${account.balance:.2f}")
        print("*****************************************************************")
        return

    print("*****************************************************************")
    if result == "NSF":
        print(f"Insufficient funds. Your balance is ${account.balance:.2f}")
    elif result == "NPAmt":
        print("Withdrawal amount must be positive.")
    else:
        print(f"Withdrawed ${amount:.2f}. New balance is ${result:.2f}")
    print("*****************************************************************")

def accountinfo(account):
    result = cursor.execute("SELECT * FROM tb_userinfo WHERE Account_id = ?;", (account.account,)).fetchone()
    print("RCL Banking System")
    print("*****************************************************************")
    if result:
        contents = {
            "Account Number": result[0],
            "First Name": result[1],
            "Last Name": result[2],
            "Gender": result[5],
            "Birthday": result[3],
            "Address": result[4],
            "Contact Number": result[6]
        }
        print(tabulate(contents.items(), tablefmt="grid"))
    else:
        print("No user found with the specified Account ID.")
    print("*****************************************************************")
    print("---------------------------")
    print("| RCL Banking System      |")
    print("|1. Update Password       |")
    print("|2. Update Address        |")
    print("|3. Update Gender         |")
    print("|4. Update Birthday       |")
    print("|5. Update Contact Number |")
    print("|0. Return to Main Page   |")
    print("---------------------------")

    choice = input("Enter your choice (1-5): ")
    if choice == '1':
        account_update(account, "Password", "tb_accounts", "id")
    elif choice == '2':
        account_update(account, "Address", "tb_userinfo", "Account_id")
    elif choice == '3':
        account_update(account, "Gender", "tb_userinfo", "Account_id")
    elif choice == '4':
        account_update(account, "Birthday", "tb_userinfo", "Account_id")
    elif choice == '5':
        account_update(account, "Contact_Number", "tb_userinfo", "Account_id")
    elif choice == '0':
        return
    else:
        print("That is not a valid choice")


def account_update(account, acc_item, tb_name, acc_id):
    updated_value = input(f"New {acc_item}: ").strip()
    query = f"UPDATE {tb_name} SET {acc_item} = ? WHERE {acc_id} = ?;"
    print("*****************************************************************")
    try:
        cursor.execute(query, (updated_value, account.account))
        connection.commit()
        print(f"Successfully updated {acc_item} to '{updated_value}'.")
    except sqlite3.Error as e:
        print(f"An error occurred while updating the account: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
    print("*****************************************************************")

if __name__ == "__main__":
    main()
