import sqlite3


import bcrypt


class UserAuthentication:
    def __init__(self, db_path: str):
        self.db_path = db_path

    def insert_user_into_db(self, username: str, password: str):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        hashed_password = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())

        try:
            cursor.execute(
                "INSERT INTO Users (username, password) VALUES (?, ?);",
                (username, hashed_password),
            )

            conn.commit()
            print("User registered successfully!")
        except sqlite3.IntegrityError:
            print("Username already exists!")
        conn.close()

    def confirm_user_details(self, username: str, password: str):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute(
            "SELECT password FROM Users WHERE username = ?;",
            (username,),
        )

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
