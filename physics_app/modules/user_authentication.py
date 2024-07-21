import sqlite3


import bcrypt


class UserAuthentication:
    def __init__(self, db_path: str):
        self.db_path = db_path

    def insert_user_into_db(self, email: str, username: str, password: str):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        hashed_password = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())
        print(
            f"Inserting into DB: email={email}, username={username}, password={hashed_password}"
        )
        try:
            cursor.execute(
                "INSERT INTO Users (email, username, password) VALUES (?, ?, ?);",
                (email, username, hashed_password),
            )

            conn.commit()
            print("User registered successfully!")
        except sqlite3.IntegrityError:
            print("Username already exists!")
        conn.close()

    def confirm_user_details(self, email_username: str, password: str):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        if "@" in email_username:
            query = "SELECT password FROM Users WHERE email = ?;"
        else:
            query = "SELECT password FROM Users WHERE username = ?;"
        cursor.execute(query, (email_username,))
        user_password = cursor.fetchone()
        conn.close()

        if user_password:
            if bcrypt.checkpw(password.encode("utf-8"), user_password[0]):
                print("Login successful!")
                return True
            else:
                print("Incorrect password!")
                return False
        else:
            print("Username does not exist!")
            return False
