import sqlite3
import os
import shutil
from datetime import datetime
import bcrypt

DB_NAME = 'manager_app.db'

# Initialize database
def initialize_db():
    try:
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()

        # Create tables if they don't exist
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE,
                password TEXT
            )
        ''')

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS transactions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT,
                type TEXT,
                amount REAL,
                category TEXT,
                date TEXT,
                FOREIGN KEY (username) REFERENCES users (username)
            )
        ''')

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS budgets (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT,
                category TEXT,
                amount REAL,
                FOREIGN KEY (username) REFERENCES users (username)
            )
        ''')

        conn.commit()
        conn.close()
    except sqlite3.Error as e:
        print(f"Error initializing database: {e}")

# Register a new user
def register_user():
    username = input("Enter a new username: ").strip()
    password = input("Enter a new password: ").strip()

    if not username or not password:
        print("Username and password cannot be empty!")
        return

    hashed_password = bcrypt.hashpw(password.encode(), bcrypt.gensalt())

    try:
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute('INSERT INTO users (username, password) VALUES (?, ?)', (username, hashed_password))
        conn.commit()
        conn.close()
        print("User registered successfully!")
    except sqlite3.IntegrityError:
        print("Username already exists. Please choose a different one.")
    except sqlite3.Error as e:
        print(f"Error registering user: {e}")

# Login user
def login_user():
    username = input("Enter your username: ").strip()
    password = input("Enter your password: ").strip()

    try:
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute('SELECT password FROM users WHERE username = ?', (username,))
        user = cursor.fetchone()
        conn.close()

        if user and bcrypt.checkpw(password.encode(), user[0]):
            print("Login successful!")
            return username
        else:
            print("Invalid username or password.")
            return None
    except sqlite3.Error as e:
        print(f"Error logging in: {e}")
        return None

# Add transaction
def add_transaction(username):
    transaction_type = input("Enter transaction type (income/expense): ").strip().lower()
    if transaction_type not in ["income", "expense"]:
        print("Invalid transaction type. Choose 'income' or 'expense'.")
        return

    try:
        amount = float(input("Enter amount: ").strip())
        category = input("Enter category (e.g., food, rent): ").strip()
        date = input("Enter date (YYYY-MM-DD, leave blank for today): ").strip() or datetime.now().strftime("%Y-%m-%d")

        # Validate date
        try:
            datetime.strptime(date, "%Y-%m-%d")
        except ValueError:
            print("Invalid date format. Use YYYY-MM-DD.")
            return

        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO transactions (username, type, amount, category, date)
            VALUES (?, ?, ?, ?, ?)
        ''', (username, transaction_type, amount, category, date))
        conn.commit()
        conn.close()
        print(f"{transaction_type.capitalize()} transaction added successfully!")
    except ValueError:
        print("Amount must be a number.")
    except sqlite3.Error as e:
        print(f"Error adding transaction: {e}")

# Update transaction
def update_transaction():
    try:
        transaction_id = int(input("Enter transaction ID to update: ").strip())
        new_amount = float(input("Enter new amount: ").strip())
        new_category = input("Enter new category: ").strip()

        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE transactions
            SET amount = ?, category = ?
            WHERE id = ?
        ''', (new_amount, new_category, transaction_id))
        conn.commit()
        conn.close()
        print("Transaction updated successfully!")
    except ValueError:
        print("Invalid input. Please provide correct values.")
    except sqlite3.Error as e:
        print(f"Error updating transaction: {e}")

# Delete transaction
def delete_transaction():
    try:
        transaction_id = int(input("Enter transaction ID to delete: ").strip())

        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute('DELETE FROM transactions WHERE id = ?', (transaction_id,))
        conn.commit()
        conn.close()
        print("Transaction deleted successfully!")
    except ValueError:
        print("Invalid input. Please enter a numeric transaction ID.")
    except sqlite3.Error as e:
        print(f"Error deleting transaction: {e}")

# Set budget
def set_budget(username):
    category = input("Enter category for the budget (e.g., food, rent): ").strip()
    try:
        amount = float(input("Enter budget amount: ").strip())

        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO budgets (username, category, amount)
            VALUES (?, ?, ?)
        ''', (username, category, amount))
        conn.commit()
        conn.close()
        print(f"Budget for {category} set to {amount}.")
    except ValueError:
        print("Amount must be a valid number.")
    except sqlite3.Error as e:
        print(f"Error setting budget: {e}")

# Update budget
def update_budget(username):
    category = input("Enter category to update the budget: ").strip()
    try:
        new_amount = float(input("Enter new budget amount: ").strip())

        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE budgets
            SET amount = ?
            WHERE username = ? AND category = ?
        ''', (new_amount, username, category))
        conn.commit()
        conn.close()
        print(f"Budget for {category} updated to {new_amount}.")
    except ValueError:
        print("Amount must be a valid number.")
    except sqlite3.Error as e:
        print(f"Error updating budget: {e}")

# Delete budget
def delete_budget(username):
    category = input("Enter category of the budget to delete: ").strip()

    try:
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute('''
            DELETE FROM budgets
            WHERE username = ? AND category = ?
        ''', (username, category))
        conn.commit()
        conn.close()
        print(f"Budget for {category} deleted successfully.")
    except sqlite3.Error as e:
        print(f"Error deleting budget: {e}")

# Logout
def logout():
    print("Logged out successfully!")
    exit()

# User menu
def user_menu(username):
    while True:
        print("\n1. Add Transaction")
        print("2. Update Transaction")
        print("3. Delete Transaction")
        print("4. Set Budget")
        print("5. Update Budget")
        print("6. Delete Budget")
        print("7. Logout")
        choice = input("Enter choice: ").strip()

        if choice == '1':
            add_transaction(username)
        elif choice == '2':
            update_transaction()
        elif choice == '3':
            delete_transaction()
        elif choice == '4':
            set_budget(username)
        elif choice == '5':
            update_budget(username)
        elif choice == '6':
            delete_budget(username)
        elif choice == '7':
            logout()
        else:
            print("Invalid choice, please try again.")

# Main function
def main():
    initialize_db()

    while True:
        print("\n1. Register")
        print("2. Login")
        print("3. Exit")
        choice = input("Enter choice: ").strip()

        if choice == '1':
            register_user()
        elif choice == '2':
            username = login_user()
            if username:
                user_menu(username)
        elif choice == '3':
            exit()
        else:
            print("Invalid choice, please try again.")

if __name__ == "__main__":
    main()
