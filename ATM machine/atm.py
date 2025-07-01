
import sqlite3
import random
import time
import logging
import csv

# Initialize Logging
logging.basicConfig(level=logging.INFO, filename='atm.log', filemode='a',
                    format='%(asctime)s - %(levelname)s - %(message)s')

# Database Initialization
db = sqlite3.connect('atm.db')
cursor = db.cursor()

# Setup Tables
def setup_database():
    cursor.execute('''CREATE TABLE IF NOT EXISTS accounts (
                        account_no INTEGER PRIMARY KEY AUTOINCREMENT,
                        name TEXT,
                        card_number TEXT UNIQUE,
                        pin TEXT,
                        balance INTEGER,
                        is_blocked INTEGER DEFAULT 0,
                        failed_attempts INTEGER DEFAULT 0
                    )''')

    cursor.execute('''CREATE TABLE IF NOT EXISTS transactions (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        card_number TEXT,
                        type TEXT,
                        amount INTEGER,
                        timestamp TEXT
                    )''')

    cursor.execute('''CREATE TABLE IF NOT EXISTS atm (
                        id INTEGER PRIMARY KEY,
                        total_cash INTEGER
                    )''')

    cursor.execute(''' CREATE TRIGGER blocked_list(
                   )''')                

    db.commit()

# Insert Default Data
def default_data():
    cursor.execute("SELECT COUNT(*) FROM accounts")
    if cursor.fetchone()[0] == 0:
        cursor.execute("INSERT INTO accounts (name, card_number, pin, balance) VALUES (?, ?, ?, ?)",
                       ("Alice", "1234567890", "1111", 100000))
        cursor.execute("INSERT INTO accounts (name, card_number, pin, balance) VALUES (?, ?, ?, ?)",
                       ("Bob", "9876543210", "2222", 50000))

    cursor.execute("SELECT COUNT(*) FROM atm")
    if cursor.fetchone()[0] == 0:
        cursor.execute("INSERT INTO atm (id, total_cash) VALUES (1, 1000000)")

    db.commit()


def log_transaction(card_number, type, amount):
    timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
    cursor.execute("INSERT INTO transactions (card_number, type, amount, timestamp) VALUES (?, ?, ?, ?)",
                   (card_number, type, amount, timestamp))
    db.commit()
    with open('atm_transactions.csv', 'a', newline='') as f:
        writer = csv.writer(f)
        writer.writerow([timestamp, card_number, type, amount])
    logging.info(f"{type} transaction for {card_number}: {amount}")



def authenticate():
    card = input("Enter Card Number: ")
    cursor.execute("SELECT pin, is_blocked, failed_attempts FROM accounts WHERE card_number=?", (card,))
    row = cursor.fetchone()
    if not row:
        print("Invalid card number.")
        return None
    pin, blocked, attempts = row
    if blocked:
        print("Account is blocked. Contact admin.")
        return None
    for i in range(3 - attempts):
        pin_input = input("Enter PIN: ")
        if pin_input == pin:
            cursor.execute("UPDATE accounts SET failed_attempts=0 WHERE card_number=?", (card,))
            db.commit()
            return card
        else:
            attempts += 1
            cursor.execute("UPDATE accounts SET failed_attempts=? WHERE card_number=?", (attempts, card))
            db.commit()
            print(f"Incorrect PIN. Attempts left: {3 - attempts}")
            if attempts >= 3:
                cursor.execute("UPDATE accounts SET is_blocked=1 WHERE card_number=?", (card,))
                db.commit()
                print("Account blocked.")
                logging.warning(f"Account {card} blocked due to multiple failed login attempts.")
                break
    return None


def user_menu(card):
    while True:
        print("\n1. View Balance\n2. Mini Statement\n3. Account Details\n4. Withdraw\n5. Deposit\n6. Transfer\n7. Fast Cash\n8. Change PIN\n9. Exit")
        choice = input("Choose option: ")

        if choice == '1':
            cursor.execute("SELECT balance FROM accounts WHERE card_number=?", (card,))
            print(f"Balance: {cursor.fetchone()[0]}")

        elif choice == '2':
            cursor.execute("SELECT type, amount, timestamp FROM transactions WHERE card_number=? ORDER BY id DESC LIMIT 5", (card,))
            for t in cursor.fetchall():
                print(t)

        elif choice == '3':
            cursor.execute("SELECT * FROM accounts WHERE card_number=?", (card,))
            print(cursor.fetchone())

        elif choice == '4':
            amount = int(input("Enter amount: "))
            cursor.execute("SELECT balance FROM accounts WHERE card_number=?", (card,))
            balance = cursor.fetchone()[0]
            cursor.execute("SELECT total_cash FROM atm WHERE id=1")
            atm_cash = cursor.fetchone()[0]
            if amount <= balance and amount <= atm_cash:
                cursor.execute("UPDATE accounts SET balance=balance-? WHERE card_number=?", (amount, card))
                cursor.execute("UPDATE atm SET total_cash=total_cash-? WHERE id=1", (amount,))
                db.commit()
                log_transaction(card, "Withdraw", amount)
                print("Withdraw successful.")
            else:
                print("Insufficient funds.")

        elif choice == '5':
            amount = int(input("Enter amount: "))
            cursor.execute("UPDATE accounts SET balance=balance+? WHERE card_number=?", (amount, card))
            cursor.execute("UPDATE atm SET total_cash=total_cash+? WHERE id=1", (amount,))
            db.commit()
            log_transaction(card, "Deposit", amount)
            print("Deposit successful.")

        elif choice == '6':
            otp = str(random.randint(1000, 9999))
            print(f"OTP: {otp}")
            user_otp = input("Enter OTP: ")
            if user_otp != otp:
                print("Invalid OTP.")
                continue
            to_card = input("Enter recipient card number: ")
            amount = int(input("Enter amount to transfer: "))
            cursor.execute("SELECT balance FROM accounts WHERE card_number=?", (card,))
            from_balance = cursor.fetchone()[0]
            cursor.execute("SELECT card_number FROM accounts WHERE card_number=?", (to_card,))
            if not cursor.fetchone():
                print("Recipient not found.")
                continue
            if from_balance >= amount:
                cursor.execute("UPDATE accounts SET balance=balance-? WHERE card_number=?", (amount, card))
                cursor.execute("UPDATE accounts SET balance=balance+? WHERE card_number=?", (amount, to_card))
                db.commit()
                log_transaction(card, "Transfer Out", amount)
                log_transaction(to_card, "Transfer In", amount)
                print("Transfer successful.")
            else:
                print("Insufficient funds.")

        elif choice == '7':
            for amt in [500, 1000, 5000]:
                print(f"{amt}")
            amount = int(input("Select Fast Cash amount: "))
            cursor.execute("SELECT balance FROM accounts WHERE card_number=?", (card,))
            balance = cursor.fetchone()[0]
            cursor.execute("SELECT total_cash FROM atm WHERE id=1")
            atm_cash = cursor.fetchone()[0]
            if amount <= balance and amount <= atm_cash:
                cursor.execute("UPDATE accounts SET balance=balance-? WHERE card_number=?", (amount, card))
                cursor.execute("UPDATE atm SET total_cash=total_cash-? WHERE id=1", (amount,))
                db.commit()
                log_transaction(card, "Fast Cash", amount)
                print("Fast Cash Withdraw successful.")
            else:
                print("Insufficient funds.")

        elif choice == '8':
            old_pin = input("Enter old PIN: ")
            cursor.execute("SELECT pin FROM accounts WHERE card_number=?", (card,))
            if cursor.fetchone()[0] == old_pin:
                new_pin = input("Enter new PIN: ")
                cursor.execute("UPDATE accounts SET pin=? WHERE card_number=?", (new_pin, card))
                db.commit()
                print("PIN updated successfully.")
            else:
                print("Incorrect old PIN.")

        elif choice == '9':
            break

        else:
            print("Invalid option.")

# Admin Panel

def admin_panel():
    password = input("Enter admin password: ")
    if password != 'admin123':
        print("Incorrect password.")
        return
    while True:
        print("\n--- Admin Panel ---\n1. Load Cash\n2. View ATM Cash\n3. View Logs\n4. Exit")
        ch = input("Enter option: ")
        if ch == '1':
            amt = int(input("Enter amount to load: "))
            cursor.execute("UPDATE atm SET total_cash=total_cash+? WHERE id=1", (amt,))
            db.commit()
            logging.info(f"Admin loaded {amt} into ATM")
            print("Cash loaded successfully.")

        elif ch == '2':
            cursor.execute("SELECT total_cash FROM atm WHERE id=1")
            print(f"ATM Total Cash: {cursor.fetchone()[0]}")

        elif ch == '3':
            with open('atm_transactions.csv', 'r') as f:
                print(f.read())

        elif ch == '4':
            break
        else:
            print("Invalid option.")

def main():
    setup_database()
    default_data()

    while True:
        print("--- Welcome to ATM Machine ---")
        print("1. User Login\n2. Admin Login\n3. Exit")
        opt = input("Choose: ")
        if opt == '1':
            card = authenticate()
            if card:
                user_menu(card)
        elif opt == '2':
            admin_panel()
        elif opt == '3':
            print("Thank you for using the services !")
            break
        else:
            print("Invalid option.")

if __name__ == "__main__":
    main()

