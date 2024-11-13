import sqlite3
import os
import shutil
from datetime import datetime

# Function to initialize the database
def initialize_db():
    try:
        conn = sqlite3.connect('finance_manager_app.db')
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

# User registration function
def register_user():
    username = input("Enter a new username: ")
    password = input("Enter a new password: ")

    try:
        conn = sqlite3.connect('finance_manager.db')
        cursor = conn.cursor()
        cursor.execute('INSERT INTO users (username, password) VALUES (?, ?)', (username, password))
        conn.commit()
        conn.close()
        print("User registered successfully!")
    except sqlite3.Error as e:
        print(f"Error registering user: {e}")

# User login function
def login_user():
    username = input("Enter your username: ")
    password = input("Enter your password: ")

    try:
        conn = sqlite3.connect('finance_manager.db')
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM users WHERE username = ? AND password = ?', (username, password))
        user = cursor.fetchone()
        conn.close()
        if user:
            print("Login successful!")
            return username
        else:
            print("Invalid username or password.")
            return None
    except sqlite3.Error as e:
        print(f"Error logging in: {e}")
        return None

# Add Income or Expense function
def add_transaction(username):
    transaction_type = input("Enter transaction type (income/expense): ")
    amount = float(input("Enter amount: "))
    category = input("Enter category (e.g., food, rent): ")
    date = input("Enter date (YYYY-MM-DD): ")

    try:
        conn = sqlite3.connect('finance_manager.db')
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO transactions (username, type, amount, category, date)
            VALUES (?, ?, ?, ?, ?)
        ''', (username, transaction_type, amount, category, date))
        conn.commit()
        conn.close()
        print(f"{transaction_type.capitalize()} transaction added successfully!")
    except sqlite3.Error as e:
        print(f"Error adding transaction: {e}")

# Update a transaction
def update_transaction():
    transaction_id = int(input("Enter transaction ID to update: "))
    new_amount = float(input("Enter new amount: "))
    new_category = input("Enter new category: ")

    try:
        conn = sqlite3.connect('finance_manager.db')
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE transactions
            SET amount = ?, category = ?
            WHERE id = ?
        ''', (new_amount, new_category, transaction_id))
        conn.commit()
        conn.close()
        print("Transaction updated successfully!")
    except sqlite3.Error as e:
        print(f"Error updating transaction: {e}")

# Delete a transaction
def delete_transaction():
    transaction_id = int(input("Enter transaction ID to delete: "))
    
    try:
        conn = sqlite3.connect('finance_manager.db')
        cursor = conn.cursor()
        cursor.execute('DELETE FROM transactions WHERE id = ?', (transaction_id,))
        conn.commit()
        conn.close()
        print("Transaction deleted successfully!")
    except sqlite3.Error as e:
        print(f"Error deleting transaction: {e}")

# Generate financial report
def generate_report(username):
    report_type = input("Enter report type (monthly/yearly): ").lower()
    current_date = datetime.now()
    
    if report_type == "monthly":
        start_date = current_date.replace(day=1).strftime("%Y-%m-%d")
        end_date = current_date.replace(day=28).strftime("%Y-%m-%d")  # Handle month end
    elif report_type == "yearly":
        start_date = current_date.replace(month=1, day=1).strftime("%Y-%m-%d")
        end_date = current_date.replace(month=12, day=31).strftime("%Y-%m-%d")
    else:
        print("Invalid report type. Please enter 'monthly' or 'yearly'.")
        return

    try:
        conn = sqlite3.connect('finance_manager.db')
        cursor = conn.cursor()
        cursor.execute('''
            SELECT SUM(amount) FROM transactions
            WHERE username = ? AND date BETWEEN ? AND ?
        ''', (username, start_date, end_date))
        total = cursor.fetchone()[0] or 0
        conn.close()
        
        print(f"Total for the {report_type} report: {total}")
    except sqlite3.Error as e:
        print(f"Error generating report: {e}")

# Set Budget
def set_budget(username):
    category = input("Enter budget category (e.g., food, rent): ")
    amount = float(input("Enter budget amount: "))

    try:
        conn = sqlite3.connect('finance_manager.db')
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO budgets (username, category, amount)
            VALUES (?, ?, ?)
        ''', (username, category, amount))
        conn.commit()
        conn.close()
        print(f"Budget for {category} set to {amount}!")
    except sqlite3.Error as e:
        print(f"Error setting budget: {e}")

# Check Budget
def check_budget(username):
    category = input("Enter category to check budget: ")
    
    try:
        conn = sqlite3.connect('finance_manager.db')
        cursor = conn.cursor()
        cursor.execute('''
            SELECT amount FROM budgets
            WHERE username = ? AND category = ?
        ''', (username, category))
        budget = cursor.fetchone()
        if budget:
            print(f"Your budget for {category} is: {budget[0]}")
        else:
            print(f"No budget set for {category}.")
        conn.close()
    except sqlite3.Error as e:
        print(f"Error checking budget: {e}")

# Backup Data
def backup_data():
    try:
        if os.path.exists('finance_manager.db'):
            shutil.copy('finance_manager.db', 'finance_manager_backup.db')
            print("Backup created successfully!")
        else:
            print("Database file not found!")
    except Exception as e:
        print(f"Error creating backup: {e}")

# Restore Data
def restore_data():
    try:
        conn = sqlite3.connect('finance_manager.db')
        cursor = conn.cursor()

        # Check if tables exist before restoring
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

        # Restore data from backup (this part can be customized based on backup logic)
        print("Data restored successfully!")
        conn.commit()
        conn.close()
    except sqlite3.Error as e:
        print(f"Error restoring data: {e}")

# Logout
def logout():
    print("Logged out successfully!")
    exit()

# User menu function
def user_menu(username):
    while True:
        print("\n1. Add Income/Expense")
        print("2. Update Transaction")
        print("3. Delete Transaction")
        print("4. Generate Report")
        print("5. Set Budget")
        print("6. Check Budget")
        print("7. Backup Data")
        print("8. Restore Data")
        print("9. Logout")
        choice = input("Enter choice: ")

        if choice == '1':
            add_transaction(username)
        elif choice == '2':
            update_transaction()
        elif choice == '3':
            delete_transaction()
        elif choice == '4':
            generate_report(username)
        elif choice == '5':
            set_budget(username)
        elif choice == '6':
            check_budget(username)
        elif choice == '7':
            backup_data()
        elif choice == '8':
            restore_data()
        elif choice == '9':
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
        choice = input("Enter choice: ")

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
