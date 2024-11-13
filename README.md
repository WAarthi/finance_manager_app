# finance_manager_app
Overview
This is a command-line application built using Python that helps users efficiently manage their personal finances. It allows users to track their income, expenses, set budgets, and generate financial reports. With the built-in database support, users can easily manage their financial data, back up and restore their information, and ensure their finances are under control.

The application is designed to be user-friendly and can be used by anyone who wants to better understand and manage their financial situation.

Features
User Registration and Authentication: Create a secure user account to manage personal finances.
Income and Expense Tracking: Record, update, and delete transactions, categorizing them into different expense or income types (e.g., food, salary, rent).
Financial Reports: Generate monthly and yearly reports to analyze income, expenses, and savings.
Budgeting: Set and track monthly budgets for various categories to control spending.
Backup and Restore: Back up data and restore it easily to ensure data integrity.
SQLite Database: The application uses an SQLite database to store user data and transaction details.
Technologies Used
Python: Programming language used to build the application.
SQLite: Database used to persist user data and transactions.
datetime: Python's built-in module used for date operations.
shutil: To handle backup and restore operations.
Installation
Clone this repository to your local machine:

bash
git clone https://github.com/your-username/finance-manager.git
Navigate to the project directory:

bash
cd finance-manager
Ensure Python 3.x is installed on your system. You can verify this by running:

bash
python --version
Run the application:

bash
python finance_manager_app.py
Usage
Upon running the application, you will be prompted to either register or log in.
Once logged in, you can:
Add Income/Expense: Track your income and expenses.
Update/Delete Transactions: Modify or remove any transaction.
Generate Reports: Get monthly or yearly financial summaries.
Set Budget: Set monthly budgets for different categories (e.g., food, entertainment).
Check Budget: View your budget for specific categories.
Backup Data: Create backups of your financial data.
Restore Data: Restore your financial data from a backup.
The app provides a simple and intuitive command-line interface to interact with your financial information.
