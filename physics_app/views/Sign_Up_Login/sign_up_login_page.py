import re
import tkinter as tk

import customtkinter as ctk
from PIL import Image


from physics_app.utilities.alert import Alert
from physics_app.utilities.setup_icons import setup_info_icon, setup_error_icon
from physics_app.utilities.show_password import PasswordEntry
from physics_app.utilities.tooltip import Tooltip
from physics_app.utilities.utilities import configure_grid, resize_and_update_image
from physics_app.views.Sign_Up_Login.forgot_password_window import (
    ForgotPasswordManager,
)
from physics_app.utilities.server_utilities.user_authentication import (
    UserAuthentication,
)


class SignUpLoginPage(tk.Frame):
    def __init__(self, parent, server_url: str, on_login_success):
        super().__init__(parent)
        self.master = parent
        self.server_url = server_url
        self.on_login_success = on_login_success
        self.user_auth = UserAuthentication(server_url)
        self.setup_master_grid()
        self.setup_icons()
        self.create_widgets()

    def setup_master_grid(self):
        self.master.grid_rowconfigure(0, weight=0)
        self.master.grid_rowconfigure(1, weight=1)
        self.master.grid_rowconfigure(2, weight=0)
        self.master.grid_columnconfigure(0, weight=0)
        self.master.grid_columnconfigure(1, weight=1)
        self.master.grid_columnconfigure(2, weight=0)

    def setup_icons(self):
        self.icon_info, self.icon_info_size = setup_info_icon()
        self.icon_error, self.icon_error_size = setup_error_icon()

    def create_widgets(self):
        ctk.set_appearance_mode("light")
        ctk.set_default_color_theme("blue")
        self.setup_center_frame()
        self.setup_canvas()
        self.setup_content_frame()
        self.setup_alert()

    def setup_center_frame(self):
        self.center_frame = ctk.CTkFrame(
            self.master, height=self.master.winfo_height(), fg_color="white"
        )
        self.center_frame.grid(row=1, column=1, sticky="nsew")
        self.center_frame.grid_rowconfigure(0, weight=1)
        self.center_frame.grid_rowconfigure(1, weight=2)
        self.center_frame.grid_rowconfigure(2, weight=1)
        self.center_frame.grid_columnconfigure(0, weight=1)
        self.center_frame.grid_columnconfigure(1, weight=1)
        self.center_frame.grid_columnconfigure(2, weight=1)

    def setup_canvas(self):
        self.canvas_for_image = ctk.CTkCanvas(
            self.center_frame,
            height=int(self.master.winfo_screenheight() / 5.5),
            borderwidth=0,
            highlightthickness=0,
            bg="white",
        )
        self.canvas_for_image.grid(row=0, column=1, sticky="nsew")
        self.image = Image.open("assets/physics_logo.png")
        self.canvas_for_image.bind("<Configure>", self.on_resize)

    def on_resize(self, event):
        resize_and_update_image(
            self.image, self.canvas_for_image, (event.width, event.height)
        )

    def setup_alert(self):
        self.alert = Alert(
            self.content_frame,
            title="Error",
            message="",
            fg_color="#fdeded",
            icon=self.icon_error,
        )
        self.alert.grid(row=2, column=1, padx=10, sticky="new")
        self.alert.hide()

    def setup_content_frame(self):
        self.content_frame = ctk.CTkFrame(self.center_frame, fg_color="white")
        self.content_frame.grid(row=1, column=1, pady=(20, 0), sticky="nsew")
        self.content_frame.grid_rowconfigure(0, weight=0)
        self.content_frame.grid_rowconfigure(1, weight=1)
        self.content_frame.grid_rowconfigure(2, weight=0)
        self.content_frame.grid_columnconfigure(0, weight=0)
        self.content_frame.grid_columnconfigure(1, weight=1)
        self.content_frame.grid_columnconfigure(2, weight=0)
        self.content_frame.grid_propagate(False)

        self.create_sign_up_widgets()
        self.create_login_widgets()
        self.sign_up_frame.tkraise()

    def create_sign_up_widgets(self):
        self.sign_up_frame = ctk.CTkFrame(
            self.content_frame,
            height=self.content_frame.winfo_height(),
            fg_color="#F1F2F3",
        )
        self.sign_up_frame.grid(row=1, column=1, sticky="n")
        configure_grid(self.sign_up_frame, rows=11, columns=3)

        self.create_sign_up_title()
        self.create_sign_up_form()
        self.create_sign_up_buttons()

    def create_sign_up_title(self):
        title = ctk.CTkLabel(
            self.sign_up_frame, text="Sign Up", font=ctk.CTkFont(size=24, weight="bold")
        )
        title.grid(row=0, column=1, pady=(10, 20), sticky="nsew")

    def create_sign_up_form(self):
        email_label = ctk.CTkLabel(
            self.sign_up_frame, text="Email:", font=ctk.CTkFont(size=14)
        )
        email_label.grid(row=1, column=1, padx=(13, 0), sticky="sw")
        self.email_entry_sign_up = ctk.CTkEntry(
            self.sign_up_frame, placeholder_text="user@email.com"
        )
        self.email_entry_sign_up.grid(row=2, column=1, padx=10, sticky="new")

        username_label = ctk.CTkLabel(
            self.sign_up_frame, text="Username:", font=ctk.CTkFont(size=14)
        )
        username_label.grid(row=3, column=1, padx=(13, 0), pady=(15, 0), sticky="sw")
        self.username_entry_sign_up = ctk.CTkEntry(
            self.sign_up_frame, placeholder_text="username"
        )
        self.username_entry_sign_up.grid(row=4, column=1, padx=10, sticky="new")

        password_label = ctk.CTkLabel(
            self.sign_up_frame, text="Password:", font=ctk.CTkFont(size=14)
        )
        password_label.grid(row=5, column=1, padx=(13, 0), pady=(15, 0), sticky="sw")

        password_info_label = ctk.CTkLabel(
            self.sign_up_frame, text="", image=self.icon_info
        )
        password_info_label.grid(
            row=5, column=1, padx=(0, 15), pady=(15, 0), sticky="se"
        )
        Tooltip(
            password_info_label,
            win_padx=69,
            text="Length at least 8 characters\n"
            "At least one uppercase letter\n"
            "At least one lowercase letter\n"
            "At least one number\n"
            "At least one special character",
            hover_delay=175,
        )
        self.password_entry_sign_up = PasswordEntry(self.sign_up_frame)
        self.password_entry_sign_up.grid(row=6, column=1, padx=10, sticky="new")

    def create_sign_up_buttons(self):
        signup_button = ctk.CTkButton(
            self.sign_up_frame,
            text="Sign Up",
            font=ctk.CTkFont(size=14, weight="bold"),
            command=self.register_user,
        )
        signup_button.grid(row=8, column=1, padx=10, pady=(20, 0), sticky="ew")

        login_label = ctk.CTkLabel(
            self.sign_up_frame,
            text="Already have an account? Log in",
            text_color="blue",
            cursor="hand2",
            font=ctk.CTkFont(size=14),
        )
        login_label.grid(row=9, column=1, padx=10, pady=(8, 0), sticky="ew")
        login_label.bind("<Button-1>", lambda e: self.show_frame(self.login_frame))

    def create_login_widgets(self):
        self.login_frame = ctk.CTkFrame(self.content_frame, fg_color="#F1F2F3")
        self.login_frame.grid(row=1, column=1, sticky="n")
        configure_grid(self.login_frame, rows=4, columns=3)

        self.create_login_title()
        self.create_login_form()
        self.create_login_buttons()

    def create_login_title(self):
        title = ctk.CTkLabel(
            self.login_frame, text="Log In", font=ctk.CTkFont(size=24, weight="bold")
        )
        title.grid(row=0, column=1, padx=10, pady=(10, 20), sticky="nsew")

    def create_login_form(self):
        username_label = ctk.CTkLabel(
            self.login_frame, text="Email:", font=ctk.CTkFont(size=14)
        )
        username_label.grid(row=1, column=1, padx=(13, 0), sticky="sw")
        self.email_entry_login = ctk.CTkEntry(
            self.login_frame, placeholder_text="Enter your email or username"
        )
        self.email_entry_login.grid(row=2, column=1, padx=10, sticky="new")

        password_label = ctk.CTkLabel(
            self.login_frame, text="Password:", font=ctk.CTkFont(size=14)
        )
        password_label.grid(row=3, column=1, padx=(13, 0), pady=(15, 0), sticky="sw")

        self.password_entry_login = PasswordEntry(self.login_frame)
        self.password_entry_login.grid(row=4, column=1, padx=10, sticky="new")

    def create_login_buttons(self):
        login_button = ctk.CTkButton(
            self.login_frame,
            text="Log In",
            font=ctk.CTkFont(size=14, weight="bold"),
            command=self.login_user,
        )
        login_button.grid(row=6, column=1, padx=10, pady=(20, 0), sticky="ew")

        signup_label = ctk.CTkLabel(
            self.login_frame,
            text="Don't have an account? Sign up",
            text_color="blue",
            cursor="hand2",
            font=ctk.CTkFont(size=14),
        )
        signup_label.grid(row=7, column=1, padx=10, pady=(8, 0), sticky="ew")
        signup_label.bind("<Button-1>", lambda e: self.show_frame(self.sign_up_frame))

        forgot_password_label = ctk.CTkLabel(
            self.login_frame,
            text="Forgot password?",
            text_color="blue",
            cursor="hand2",
            font=ctk.CTkFont(size=14),
        )
        forgot_password_label.grid(row=5, column=1, padx=(0, 13), sticky="se")
        forgot_password_label.bind(
            "<Button-1>",
            lambda e: ForgotPasswordManager(
                self.master,
                self.server_url,
                email=(
                    self.email_entry_login.get().strip()
                    if self.email_entry_login.get().strip()
                    else None
                ),
            ).setup_forgot_password_window(),
        )

    def register_user(self):
        email = self.email_entry_sign_up.get().strip()
        username = self.username_entry_sign_up.get().strip()
        password = self.password_entry_sign_up.get_entry()
        error_messages = self.validate_registration(email, username, password)

        if error_messages:
            self.show_error_alert("\n".join(error_messages))
            return

        self.alert.hide()
        self.user_auth.register_user(email, username, password)
        self.show_frame(self.login_frame)

    def validate_registration(self, email, username, password):
        error_messages = []
        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            error_messages.append("Invalid email format.")
        if len(username) == 0 or len(username) > 20:
            error_messages.append("Username must be between 1 and 20 characters.")
        if not re.match(
            r"^(?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*[!@#$%^&*()_+=\{\[\]\\|:;'<>/?~]).{8,}$",
            password,
        ):
            error_messages.append(
                "Password must be at least 8 characters long and contain capital and lowercase letters, numbers, and a special character."
            )
        if self.user_auth.is_email_taken(email):
            error_messages.append("Email is already registered.")
        if self.user_auth.is_username_taken(username):
            error_messages.append("Username is already taken.")
        return error_messages

    def login_user(self):
        email_username = self.email_entry_login.get()
        password = self.password_entry_login.get_entry()
        error_messages = self.validate_login(email_username, password)

        if error_messages:
            self.show_error_alert("\n".join(error_messages))
            return

        self.alert.hide()
        if not self.user_auth.login_user(email_username, password):
            self.show_error_alert("Incorrect Email or Password", "Login Failed")
        else:
            user_id = self.user_auth.get_user_id(email_username)
            if user_id:
                self.on_login_success(user_id)
            else:
                print("Failed to retrieve user ID")

    def validate_login(self, email_username, password):
        error_messages = []
        if not email_username:
            error_messages.append("Email/Username cannot be empty.")
        if not password:
            error_messages.append("Password cannot be empty.")
        return error_messages

    def show_frame(self, frame):
        self.clear_entries()
        self.alert.hide()
        (
            self.sign_up_frame.grid_forget()
            if frame == self.login_frame
            else self.login_frame.grid_forget()
        )
        frame.grid(row=1, column=1, sticky="n")
        frame.tkraise()

    def clear_entries(self):
        entries = [
            (self.email_entry_sign_up, "user@email.com"),
            (self.username_entry_sign_up, "username"),
            (self.email_entry_login, "Enter your email or username"),
        ]
        for entry, placeholder in entries:
            entry.delete(0, tk.END)
            entry.configure(placeholder_text=placeholder)

        self.password_entry_sign_up.clear_entry()
        self.password_entry_login.clear_entry()

    def show_error_alert(self, message, title="Error"):
        self.alert.update_text(new_title=title, new_message=message)
        self.alert.show(row=2, column=1, padx=10, sticky="new")
