import sqlite3
from datetime import datetime


# Function to create a SQLite database and the "users" table
def create_table():
    conn = sqlite3.connect("../database.sqlite3")
    c = conn.cursor()
    c.execute(
        """CREATE TABLE IF NOT EXISTS users 
                 (row_id INTEGER PRIMARY KEY, telegram_id INTEGER, token TEXT, date_created TEXT)"""
    )
    conn.commit()
    conn.close()


# Function to insert a new user into the "users" table
def insert_user(telegram_id, token):
    conn = sqlite3.connect("../db.sqlite3")
    c = conn.cursor()
    date_created = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    c.execute(
        """INSERT INTO users (telegram_id, token, date_created) 
                 VALUES (?, ?, ?)""",
        (telegram_id, token, date_created),
    )
    conn.commit()
    conn.close()


# Function to retrieve all users from the "users" table
def get_all_users():
    conn = sqlite3.connect("../db.sqlite3")
    c = conn.cursor()
    c.execute("""SELECT * FROM users""")
    rows = c.fetchall()
    conn.close()
    return rows


# Function to retrieve a specific user by their Telegram ID
def get_user_by_telegram_id(telegram_id):
    conn = sqlite3.connect("../db.sqlite3")
    c = conn.cursor()
    c.execute("""SELECT * FROM users WHERE telegram_id = ?""", (telegram_id,))
    row = c.fetchone()
    conn.close()
    return row


# Function to update the token of a user
def update_token(telegram_id, new_token):
    conn = sqlite3.connect("../db.sqlite3")
    c = conn.cursor()
    c.execute(
        """UPDATE users SET token = ? WHERE telegram_id = ?""", (new_token, telegram_id)
    )
    conn.commit()
    conn.close()


# Function to delete a user by their Telegram ID
def delete_user(telegram_id):
    conn = sqlite3.connect("../db.sqlite3")
    c = conn.cursor()
    c.execute("""DELETE FROM users WHERE telegram_id = ?""", (telegram_id,))
    conn.commit()
    conn.close()


# Example usage:
if __name__ == "__main__":
    create_table()

    # Inserting a new user
    insert_user(123456789, "example_token")

    # Retrieving all users
    print(get_all_users())

    # Retrieving a specific user by their Telegram ID
    print(get_user_by_telegram_id(123456789))

    # Updating the token of a user
    update_token(123456789, "new_example_token")

    # Deleting a user by their Telegram ID
    delete_user(123456789)

    # Retrieving all users after deletion
    print(get_all_users())
