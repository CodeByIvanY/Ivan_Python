# RCL Banking System
#### Video Demo:  <[RCL Banking System](https://www.youtube.com/watch?v=6WHVJJLA8_Y)>
#### Description

The RCL Banking System is a simple command-line banking application built using Python and SQLite. It allows users to manage their accounts, perform transactions such as deposits and withdrawals, and view their account information. The application is designed to be user-friendly and provides a basic interface for banking operations.


## Features
* User login and sign-up functionality
* Deposit and withdrawal operations
* Balance inquiry
* User information display and update

## Requirements
* Python 3.x
* SQLite3
* Tabulate library (for formatted output)

## Usage
1. Run the application:
2. Follow the on-screen prompts to log in or sign up for a new account.
3. Once logged in, you can:
    * Check your balance
    * Deposit money into your account
    * Withdraw money from your account
    * Veiw and update your account information.
### Sign Up
The application prompts users for various inputs, including:
1. First Name
2. Last Name
3. Password (minimum 8 characters)
4. Gender (optional)
5. Birthday (optional)
6. Address (optional)
7. Contact Number (optional)

## Code Structure
* **Account Class**: Manages account details and transactions.
* **Main Function**: Controls the flow of the application, handling user input and displaying menus.
    * **login(account)**: Handles user login.
    * **sign_out(account)**: Manages user account creation.
* **Transaction Functions**: Includes functions for depositing, withdrawing, and displaying account information.
    * **deposit(account)**: Processes deposit transactions.
    * **withdraw(account)**: Processes withdrawal transactions.
    * **show_balance(balance)**: Displays the user's current balance.
    * **accountinfo(account)**: Shows user account information and allows updates.
    * **account_update(account, acc_item, tb_name, acc_id)**: Updates specific account information.

## Database Schema
The application uses a SQLite database with the following tables:

* tb_accounts: Stores account credentials and hashed passwords.
* tb_userinfo: Stores user personal information.
* tb_transactions: Logs all transactions made by the user.
```
CREATE TABLE "tb_accounts" (
    "id" NUMERIC,
    "Password" TEXT NOT NULL,
    "is_deleted" BOOLEAN NOT NULL DEFAULT 0 CHECK ("is_deleted" IN (0, 1)),
    PRIMARY KEY ("id")
);
```
```
CREATE TABLE "tb_userinfo" (
    "Account_id" NUMERIC,
    "First_Name" TEXT CHECK(length(First_Name) < 50),
    "Last_Name" TEXT CHECK(length(Last_Name) < 50),
    "Birthday" TEXT CHECK(length(Last_Name) < 50),,
    "Address" TEXT,
    "Gender" TEXT CHECK("Gender" IN ('M', 'F')),
    "Contact_Number" TEXT CHECK(length(First_Name) < 20),
    "is_deleted" BOOLEAN NOT NULL DEFAULT 0 CHECK ("is_deleted" IN (0, 1)),
    FOREIGN KEY("Account_id") REFERENCES "tb_accounts"("id") ON DELETE CASCADE
);
```
```
CREATE TABLE "tb_transactions" (
    "Account_id" NUMERIC,
    "TransType" TEXT NOT NULL CHECK ("TransType" IN ('Deposit', 'Withdraw', 'TransferIn','TransferOut')),
    "Amount" NUMBERIC(5,2) NOT NULL CHECK("Amount" != 0),
    "DateTime" NUMERIC NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "is_deleted" BOOLEAN NOT NULL DEFAULT 0 CHECK ("is_deleted" IN (0, 1)),
    FOREIGN KEY("Account_id") REFERENCES "tb_accounts"("id") ON DELETE CASCADE
);
```
## Error Handling
The application includes error handling for various scenarios, such as:
* Invalid login credentials
* Insufficient funds for withdrawal
* Non-positive amounts for deposits and withdrawals
* Database errors during transactions
