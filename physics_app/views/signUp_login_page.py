import re
import threading
import tkinter as tk

import customtkinter as ctk
import requests
from PIL import Image, ImageTk

from physics_app.modules.user_authentication import UserAuthentication
from physics_app.utilities.alert import Alert
from physics_app.utilities.setup_icons import (
    setup_info_icon,
    setup_error_icon,
)
from physics_app.utilities.tooltip import Tooltip
from physics_app.utilities.utilities import (
    request_verification_code,
    request_verify_otp,
)


class SignUpLoginPage(tk.Frame):
    def __init__(self, master, auth: UserAuthentication):
        super().__init__(master)
        self.master = master
        self.auth = auth
        self.master.grid_rowconfigure(0, weight=0)
        self.master.grid_rowconfigure(1, weight=1)
        self.master.grid_rowconfigure(2, weight=0)
        self.master.grid_columnconfigure(0, weight=0)
        self.master.grid_columnconfigure(1, weight=1)
        self.master.grid_columnconfigure(2, weight=0)
        self.master.configure(bg="white")
        self.icon_info, self.icon_info_size = setup_info_icon()
        self.icon_error, self.icon_error_size = setup_error_icon()
        self.create_widgets()

    def create_widgets(self):
        self.setup_appearance()
        self.setup_center_frame()
        self.setup_canvas()
        self.setup_alert()
        self.setup_content_frame()
        self.create_sign_up_widgets()
        self.create_login_widgets()
        self.sign_up_frame.tkraise()

    def setup_appearance(self):
        ctk.set_appearance_mode("light")
        ctk.set_default_color_theme("blue")

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
        self.canvas_for_image.bind("<Configure>", self.resize_image)

    def setup_alert(self):
        self.alert = Alert(
            self.center_frame,
            title="Error",
            message="",
            fg_color="#fdeded",
            icon=self.icon_error,
        )
        self.alert.grid(row=2, column=1, padx=10, sticky="new")
        self.alert.hide()

    def setup_content_frame(self):
        self.content_frame = ctk.CTkFrame(
            self.center_frame,
            fg_color="white",
        )
        self.content_frame.grid(row=1, column=1, pady=(20, 20), sticky="nsew")
        self.content_frame.grid_rowconfigure(0, weight=0)
        self.content_frame.grid_rowconfigure(1, weight=1)
        self.content_frame.grid_rowconfigure(2, weight=0)
        self.content_frame.grid_columnconfigure(0, weight=0)
        self.content_frame.grid_columnconfigure(1, weight=1)
        self.content_frame.grid_columnconfigure(2, weight=0)
        self.content_frame.grid_propagate(False)

    def create_sign_up_widgets(self):
        self.sign_up_frame = ctk.CTkFrame(
            self.content_frame,
            height=self.content_frame.winfo_height(),
            fg_color="#F1F2F3",
        )
        self.sign_up_frame.grid(row=1, column=1, sticky="n")

        self.configure_grid(self.sign_up_frame, rows=11, columns=3)

        title = ctk.CTkLabel(
            self.sign_up_frame, text="Sign Up", font=ctk.CTkFont(size=24, weight="bold")
        )
        title.grid(row=0, column=1, pady=(10, 20), sticky="nsew")

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

        password_info_label_tooltip = Tooltip(
            password_info_label,
            text="Length at least 8 characters\n"
            "At least one uppercase letter\n"
            "At least one lowercase letter\n"
            "At least one number\n"
            "At least one special character",
            hover_delay=175,
        )
        self.password_entry_sign_up = ctk.CTkEntry(
            self.sign_up_frame, show="*", placeholder_text="*****"
        )
        self.password_entry_sign_up.grid(row=6, column=1, padx=10, sticky="new")

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

        self.configure_grid(self.login_frame, rows=4, columns=3)

        title = ctk.CTkLabel(
            self.login_frame, text="Log In", font=ctk.CTkFont(size=24, weight="bold")
        )
        title.grid(row=0, column=1, padx=10, pady=(10, 20), sticky="nsew")

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
        forgot_password_label = ctk.CTkLabel(
            self.login_frame,
            text="Forgot password?",
            text_color="blue",
            cursor="hand2",
            font=ctk.CTkFont(size=14),
        )
        forgot_password_label.grid(row=5, column=1, padx=(0, 13), sticky="se")
        forgot_password_label.bind(
            "<Button-1>", lambda e: self.forgot_password_widgets()
        )

        self.password_entry_login = ctk.CTkEntry(
            self.login_frame, show="*", placeholder_text="*****"
        )
        self.password_entry_login.grid(row=4, column=1, padx=10, sticky="new")

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

    def forgot_password_widgets(self):
        # Get the position and size of the root window
        root_x = self.master.winfo_rootx()
        root_y = self.master.winfo_rooty()
        root_width = self.master.winfo_width()
        root_height = self.master.winfo_height()

        # Calculate the center position of the screen
        center_x = root_x + (root_width // 2)
        center_y = root_y + (root_height // 2)

        # Create the forgot password window and set its position
        self.forgot_password_window = ctk.CTkToplevel(self.master)
        self.forgot_password_window.attributes("-topmost", 1)
        self.forgot_password_window.title("Forgot Password")

        # Set the geometry to center the window on the monitor
        self.forgot_password_window.geometry(f"+{center_x}+{center_y}")

        # Rest of your forgot password UI code...

        self.forgot_password_center_frame = ctk.CTkFrame(
            self.forgot_password_window, fg_color="#F1F2F3"
        )
        self.forgot_password_center_frame.grid(row=0, column=0, sticky="nsew")
        self.forgot_password_center_frame.grid(row=0, column=0, sticky="nsew")
        self.forgot_password_center_frame.grid_rowconfigure(0, weight=1)
        self.forgot_password_center_frame.grid_rowconfigure(1, weight=2)
        self.forgot_password_center_frame.grid_rowconfigure(2, weight=1)
        self.forgot_password_center_frame.grid_columnconfigure(0, weight=1)
        self.forgot_password_center_frame.grid_columnconfigure(1, weight=1)
        self.forgot_password_center_frame.grid_columnconfigure(2, weight=1)

        self.create_send_code_frame()

        self.create_enter_code_frame()

        self.send_code_frame.tkraise()

    def create_send_code_frame(self):
        self.send_code_frame = ctk.CTkFrame(
            self.forgot_password_center_frame, fg_color="#F1F2F3"
        )
        self.send_code_frame.grid(row=1, column=1, pady=(20, 20), sticky="nsew")
        self.configure_grid(self.send_code_frame, rows=5, columns=0)

        title = ctk.CTkLabel(
            self.send_code_frame,
            text="Reset your password",
            font=ctk.CTkFont(size=24, weight="bold"),
        )
        title.grid(row=0, column=0, padx=10, pady=(10, 20), sticky="nsew")
        message = ctk.CTkLabel(
            self.send_code_frame,
            text="Enter the email you signed up with. We'll send you a one time code to enter to reset your password.",
            wraplength=240,
            font=ctk.CTkFont(size=14),
        )
        message.grid(row=1, column=0, padx=5, sticky="nsew")

        email_label = ctk.CTkLabel(
            self.send_code_frame, text="Email:", font=ctk.CTkFont(size=14)
        )
        email_label.grid(row=2, column=0, padx=(13, 0), sticky="sw")

        self.email_entry_forgot_password = ctk.CTkEntry(
            self.send_code_frame,
        )
        self.email_entry_forgot_password.grid(row=3, column=0, padx=10, sticky="new")
        self.email_entry_forgot_password.insert(
            0, self.email_entry_login.get() if self.email_entry_login.get() else ""
        )

        verify_button = ctk.CTkButton(
            self.send_code_frame,
            text="Send Verification Code",
            font=ctk.CTkFont(size=14, weight="bold"),
            command=self.on_send_code_click,
        )
        verify_button.grid(row=4, column=0, padx=10, pady=(20, 0), sticky="ew")

    def create_enter_code_frame(self):
        self.enter_code_frame = ctk.CTkFrame(
            self.forgot_password_center_frame, fg_color="#F1F2F3"
        )
        self.enter_code_frame.grid(row=1, column=1, pady=(20, 20), sticky="nsew")
        self.configure_grid(self.enter_code_frame, rows=6, columns=0)

        title = ctk.CTkLabel(
            self.enter_code_frame,
            text="Reset your password",
            font=ctk.CTkFont(size=24, weight="bold"),
        )
        title.grid(row=0, column=0, padx=10, pady=(10, 20), sticky="nsew")
        code_label = ctk.CTkLabel(
            self.enter_code_frame,
            text="Enter Verification Code:",
            font=ctk.CTkFont(size=14),
        )
        code_label.grid(row=1, column=0, padx=(13, 0), sticky="sw")

        self.code_entry = ctk.CTkEntry(
            self.enter_code_frame,
        )
        self.code_entry.grid(row=2, column=0, padx=10, sticky="new")

        self.timer_label = ctk.CTkLabel(
            self.enter_code_frame, text="", font=ctk.CTkFont(size=14)
        )
        self.timer_label.grid(row=3, column=0, padx=10, pady=(10, 0), sticky="ew")

        submit_button = ctk.CTkButton(
            self.enter_code_frame,
            text="Submit",
            font=ctk.CTkFont(size=14, weight="bold"),
            command=self.on_submit_code_click,
        )
        submit_button.grid(row=4, column=0, padx=10, pady=(20, 0), sticky="ew")

        self.resend_label = ctk.CTkLabel(
            self.enter_code_frame,
            text="Resend Email",
            text_color="blue",
            cursor="hand2",
            font=ctk.CTkFont(size=14),
        )
        self.resend_label.grid(row=5, column=0, padx=10, pady=(10, 0), sticky="ew")
        self.resend_label.bind("<Button-1>", lambda e: self.resend_verification_code())

    def on_send_code_click(self):
        email = self.email_entry_forgot_password.get().strip()
        if not email or not self.auth.is_email_taken(email):
            print("Error", "Please enter your email address.")
            return

        if request_verification_code(email):
            self.enter_code_frame.tkraise()
            self.start_timer()

    def on_submit_code_click(self):
        email = self.email_entry_forgot_password.get().strip()
        code = self.code_entry.get().strip()
        if not code:
            print("Error", "Please enter the verification code.")
            return

        if request_verify_otp(email, code):
            print("Success", "Verification successful!")
            # self.reset_password_frame.tkraise()  # Navigate to the password reset frame or next step

    def resend_verification_code(self):
        self.send_code_frame.tkraise()
        self.start_timer()

    def start_timer(self):
        self.time_left = 60
        self.resend_label.configure(text_color="grey", cursor="arrow")
        self.resend_label.unbind("<Button-1>")  # Disable clicking functionality
        self.update_timer()

    def update_timer(self):
        if hasattr(self, "timer") and self.timer:
            self.timer.cancel()  # Cancel any existing timer to prevent overlap

        if self.time_left > 0:
            self.timer_label.configure(text=f"Resend code in {self.time_left} seconds")
            self.time_left -= 1
            self.timer = threading.Timer(1.0, self.update_timer)
            self.timer.start()
        else:
            self.timer_label.configure(text="You can resend the code now")
            self.resend_label.configure(text_color="blue", cursor="hand2")
            self.resend_label.bind(
                "<Button-1>", lambda e: self.resend_verification_code()
            )  # Re-enable clicking

    def configure_grid(self, frame, rows, columns):
        for i in range(columns):
            frame.grid_columnconfigure(i, weight=1)
        for i in range(1, rows):
            frame.grid_rowconfigure(i, weight=1)

    def register_user(self):
        email = self.email_entry_sign_up.get().strip()
        username = self.username_entry_sign_up.get().strip()
        password = self.password_entry_sign_up.get()

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
                "Password must be at least 8 characters long and contain both letters and numbers."
            )

        if self.auth.is_email_taken(email):
            error_messages.append("Email is already registered.")

        if self.auth.is_username_taken(username):
            error_messages.append("Username is already taken.")

        if error_messages:
            self.alert.update_text(
                new_title="Error",
                new_message="\n".join(error_messages),
            )
            self.alert.show(row=2, column=1, padx=10, sticky="new")
            return
        self.alert.hide()
        self.auth.insert_user_into_db(email, username, password)
        self.show_frame(self.login_frame)

    def login_user(self):
        email_username = self.email_entry_login.get()
        password = self.password_entry_login.get()

        error_messages = []

        if not email_username:
            error_messages.append("Email/Username cannot be empty.")

        if not password:
            error_messages.append("Password cannot be empty.")

        if error_messages:
            self.alert.update_text(
                new_title="Error",
                new_message="\n".join(error_messages),
            )
            self.alert.show(row=2, column=1, padx=10, sticky="new")
            return
        self.alert.hide()
        self.auth.confirm_user_details(email_username, password)

    def show_frame(self, frame):
        self.clear_entries()
        if frame == self.sign_up_frame:
            self.login_frame.grid_forget()
            self.sign_up_frame.grid(row=1, column=1, sticky="n")
            self.sign_up_frame.tkraise()
        else:
            self.alert.hide()
            self.sign_up_frame.grid_forget()
            self.login_frame.grid(row=1, column=1, sticky="n")
            self.login_frame.tkraise()

    def clear_entries(self):
        entries = [
            (self.email_entry_sign_up, "user@email.com"),
            (self.username_entry_sign_up, "username"),
            (self.password_entry_sign_up, "*****"),
            (self.email_entry_login, "Enter your email or username"),
            (self.password_entry_login, "*****"),
        ]
        for entry, placeholder in entries:
            entry.delete(0, tk.END)
            entry.configure(placeholder_text=placeholder)

    def resize_image(self, event):
        new_width = int(event.width / 1.5)
        new_height = int((self.image.height / self.image.width) * new_width)
        if new_height > event.height:
            new_height = event.height
            new_width = int(new_height / (self.image.height / self.image.width))
        resized_image = self.image.resize(
            (new_width, new_height), Image.Resampling.LANCZOS
        )
        self.image_tk = ImageTk.PhotoImage(resized_image)
        self.canvas_for_image.create_image(
            event.width // 2, event.height // 2, image=self.image_tk, anchor="center"
        )
