# login_page.py
import tkinter as tk
from tkinter import ttk

from physics_app.modules.user_authentication import UserAuthentication


class SignUpLoginPage(tk.Frame):
    def __init__(self, master, auth: UserAuthentication):
        super().__init__(master)
        self.auth = auth
        self.create_widgets()

    def create_widgets(self):
        self.register_button = ttk.Button(
            self, text="Register", command=self.register_user
        )
        self.register_button.pack()

        self.login_button = ttk.Button(self, text="Login", command=self.login_user)
        self.login_button.pack()

    def register_user(self):
        username = "test_user"
        password = "test_password"
        self.auth.insert_user_into_db(username, password)

    def login_user(self):
        username = "test_user"
        password = "test_password"
        self.auth.confirm_user_details(username, password)
