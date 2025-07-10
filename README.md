Here's an aesthetically appealing and detailed README file for your ATM project, ready for GitHub\!

-----

# 💰 Python ATM Machine Simulator

An interactive command-line ATM (Automated Teller Machine) simulator built with Python and SQLite. This project mimics core ATM functionalities like balance inquiry, withdrawals, deposits, transfers, and includes a secure login system with an admin panel.

-----

## ✨ Features

### User Functionality:

  * **Secure Authentication**: Log in with a card number and PIN. Multiple incorrect attempts lead to account blocking.
  * **Account Management**:
      * **View Balance**: Check your current account balance instantly.
      * **Mini Statement**: See your last 5 transactions.
      * **Account Details**: View your full account information.
      * **Withdraw Cash**: Get cash, subject to account balance and ATM's available funds.
      * **Deposit Cash**: Add funds to your account.
      * **Transfer Funds**: Securely transfer money to another account (with a simulated OTP for added security).
      * **Fast Cash**: Quick withdrawals for predefined amounts.
      * **Change PIN**: Update your PIN for enhanced security.
  * **Transaction Logging**: All transactions are recorded for auditing and statement generation.

### Admin Panel:

  * **Secure Access**: Protected by an admin password.
  * **ATM Management**:
      * **Load Cash**: Replenish the ATM's cash reserves.
      * **View ATM Cash**: Check the current cash available in the ATM.
  * **Activity Monitoring**: View all ATM transactions from a CSV log.

### Robust Backend:

  * **SQLite Database**: `atm.db` for persistent storage of account, transaction, and ATM data.
  * **Logging**: `atm.log` captures all significant system events and transactions.
  * **CSV Reports**: `atm_transactions.csv` provides a clear, spreadsheet-compatible record of all financial activities.

-----

## 🛠️ Technologies Used

  * **Python 3.x**: The core programming language.
  * **`sqlite3`**: Python's built-in module for SQLite database interaction.
  * **`logging`**: For comprehensive event logging.
  * **`csv`**: For generating transaction reports.
  * **`random`**: Used for simulating OTP generation during transfers.
  * **`time`**: For timestamping transactions.

-----

## 🚀 Getting Started

Follow these steps to set up and run the ATM simulator on your local machine.

### Prerequisites

  * Python 3.x installed on your system.

### Installation

1.  **Clone the repository** (or copy the code into a file named `atm_simulator.py`):

    ```bash
    git clone https://github.com/YourGitHubUsername/atm-machine-simulator.git
    cd atm-machine-simulator
    ```

    (If you don't have a GitHub repo yet, just save the code as `atm_simulator.py`)

2.  **Run the application**:

    ```bash
    python atm_simulator.py
    ```

-----

## 📖 How to Use

When you run the `atm_simulator.py` script, you will be presented with the main menu:

```
--- Welcome to ATM Machine ---
1. User Login
2. Admin Login
3. Exit
Choose:
```

### User Login (Option 1)

1.  **Enter Card Number**: Use one of the default card numbers: `1234567890` or `9876543210`.
2.  **Enter PIN**: Use the corresponding default PINs: `1111` (for `1234567890`) or `2222` (for `9876543210`).
      * **Security Feature**: After 3 incorrect PIN attempts, the account will be blocked. Contact an administrator to unblock it.
3.  Upon successful login, you'll see the user menu with various transaction options.

### Admin Login (Option 2)

1.  **Enter Admin Password**: The default admin password is `admin123`.
2.  Once logged in, you can manage ATM cash or view transaction logs.

### Default Accounts

For easy testing, the system comes pre-loaded with two accounts:

| Name  | Card Number | PIN  | Initial Balance |
| :---- | :---------- | :--- | :-------------- |
| Alice | 1234567890  | 1111 | 100000          |
| Bob   | 9876543210  | 2222 | 50000           |

The ATM initially contains `1,000,000` cash.

-----

## 🗄️ Database Schema

The application uses an SQLite database named `atm.db` with three tables:

  * ### `accounts`

      * `account_no` (INTEGER PRIMARY KEY AUTOINCREMENT): Unique account identifier.
      * `name` (TEXT): Account holder's name.
      * `card_number` (TEXT UNIQUE): Unique 10-digit card number.
      * `pin` (TEXT): 4-digit PIN for authentication.
      * `balance` (INTEGER): Current account balance.
      * `is_blocked` (INTEGER DEFAULT 0): 0 for active, 1 for blocked.
      * `failed_attempts` (INTEGER DEFAULT 0): Counts consecutive failed PIN attempts.

  * ### `transactions`

      * `id` (INTEGER PRIMARY KEY AUTOINCREMENT): Unique transaction ID.
      * `card_number` (TEXT): The card number involved in the transaction.
      * `type` (TEXT): Type of transaction (e.g., 'Withdraw', 'Deposit', 'Transfer Out', 'Transfer In', 'Fast Cash').
      * `amount` (INTEGER): Amount of money involved in the transaction.
      * `timestamp` (TEXT): Date and time of the transaction.

  * ### `atm`

      * `id` (INTEGER PRIMARY KEY): Fixed to 1.
      * `total_cash` (INTEGER): Current total cash available in the ATM machine.

-----

## 📊 Logs & Reports

  * **`atm.log`**: This file records all significant events, including successful logins, failed attempts, account blocking, and admin actions.
  * **`atm_transactions.csv`**: A CSV file that logs every financial transaction. This provides a clean, structured record for easy analysis or external reporting.

-----

## 🤝 Contributing

Contributions are welcome\! If you have ideas for improvements, new features, or bug fixes, feel free to:

1.  Fork the repository.
2.  Create a new branch (`git checkout -b feature/your-feature`).
3.  Make your changes.
4.  Commit your changes (`git commit -m 'Add new feature'`).
5.  Push to the branch (`git push origin feature/your-feature`).
6.  Open a Pull Request.

-----

## 📄 License

This project is open-source and available under the [MIT License](https://www.google.com/search?q=LICENSE).

-----
