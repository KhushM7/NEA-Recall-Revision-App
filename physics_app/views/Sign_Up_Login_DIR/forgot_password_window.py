import re
import threading
from typing import Optional

import customtkinter as ctk
from physics_app.utilities.tooltip import Tooltip
from physics_app.utilities.server_utilities import (
    request_verification_code,
    request_verify_otp,
)
from physics_app.modules.user_authentication import UserAuthentication as Auth
from physics_app.utilities.setup_icons import setup_info_icon
from physics_app.utilities.utilities import configure_grid


class ForgotPasswordManager:
    def __init__(self, master, auth: Auth, email: str = None) -> None:
        self.master = master
        self.auth = auth
        self.email = email
        self.icon_info, self.icon_info_size = setup_info_icon()

        self.forgot_password_window: Optional[ctk.CTkToplevel] = None
        self.forgot_password_center_frame: Optional[ctk.CTkFrame] = None
        self.send_code_frame: Optional[ctk.CTkFrame] = None
        self.enter_code_frame: Optional[ctk.CTkFrame] = None
        self.reset_password_frame: Optional[ctk.CTkFrame] = None

        self.email_entry_forgot_password: Optional[ctk.CTkEntry] = None
        self.code_entry: Optional[ctk.CTkEntry] = None
        self.password_entry_forgot_password: Optional[ctk.CTkEntry] = None
        self.confirm_password_entry_forgot_password: Optional[ctk.CTkEntry] = None

        self.error_label: Optional[ctk.CTkLabel] = None
        self.error_label_otp: Optional[ctk.CTkLabel] = None
        self.error_label_password: Optional[ctk.CTkLabel] = None
        self.timer_label: Optional[ctk.CTkLabel] = None
        self.resend_label: Optional[ctk.CTkLabel] = None

        self.time_left: int = 60
        self.timer: Optional[threading.Timer] = None

    def setup_forgot_password_window(self) -> None:
        root_x = self.master.winfo_rootx()
        root_y = self.master.winfo_rooty()
        root_width = self.master.winfo_width()
        root_height = self.master.winfo_height()

        center_x = root_x + (root_width // 2)
        center_y = root_y + (root_height // 2)

        self.forgot_password_window = ctk.CTkToplevel(self.master)
        self.forgot_password_window.attributes("-topmost", 1)
        self.forgot_password_window.title("Forgot Password")
        self.forgot_password_window.geometry(f"+{center_x}+{center_y}")

        self.forgot_password_center_frame = ctk.CTkFrame(
            self.forgot_password_window, fg_color="#F1F2F3"
        )
        self.forgot_password_center_frame.grid(row=0, column=0, sticky="nsew")
        self.forgot_password_center_frame.grid_rowconfigure(0, weight=1)
        self.forgot_password_center_frame.grid_rowconfigure(1, weight=2)
        self.forgot_password_center_frame.grid_rowconfigure(2, weight=1)
        self.forgot_password_center_frame.grid_columnconfigure(0, weight=1)
        self.forgot_password_center_frame.grid_columnconfigure(1, weight=1)
        self.forgot_password_center_frame.grid_columnconfigure(2, weight=1)

        self.create_send_code_frame()
        self.create_enter_code_frame()
        self.create_reset_password_frame()
        self.send_code_frame.tkraise()

    def create_send_code_frame(self) -> None:
        self.send_code_frame = ctk.CTkFrame(
            self.forgot_password_center_frame, fg_color="#F1F2F3"
        )
        self.send_code_frame.grid(row=1, column=1, pady=(20, 20), sticky="nsew")
        configure_grid(self.send_code_frame, rows=6, columns=0)

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

        self.email_entry_forgot_password = ctk.CTkEntry(self.send_code_frame)
        self.email_entry_forgot_password.insert(
            0, "" if self.email is None else self.email
        )
        self.email_entry_forgot_password.grid(
            row=3, column=0, padx=10, pady=0, sticky="new"
        )

        self.error_label = ctk.CTkLabel(
            self.send_code_frame,
            text="",
            text_color="red",
            font=ctk.CTkFont(size=12),
        )
        self.error_label.grid(row=4, column=0, padx=10, pady=(0, 0), sticky="nw")

        verify_button = ctk.CTkButton(
            self.send_code_frame,
            text="Send Verification Code",
            font=ctk.CTkFont(size=14, weight="bold"),
            command=self.on_send_code_click,
        )
        verify_button.grid(row=5, column=0, padx=10, pady=(20, 0), sticky="ew")

    def create_enter_code_frame(self) -> None:
        self.enter_code_frame = ctk.CTkFrame(
            self.forgot_password_center_frame, fg_color="#F1F2F3"
        )
        self.enter_code_frame.grid(row=1, column=1, pady=(20, 20), sticky="nsew")
        configure_grid(self.enter_code_frame, rows=7, columns=0)

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

        self.code_entry = ctk.CTkEntry(self.enter_code_frame)
        self.code_entry.grid(row=2, column=0, padx=10, sticky="new")

        self.error_label_otp = ctk.CTkLabel(
            self.enter_code_frame,
            text="",
            text_color="red",
            font=ctk.CTkFont(size=12),
        )
        self.error_label_otp.grid(row=3, column=0, padx=10, pady=(5, 0), sticky="nw")

        self.timer_label = ctk.CTkLabel(
            self.enter_code_frame, text="", font=ctk.CTkFont(size=14)
        )
        self.timer_label.grid(row=4, column=0, padx=10, pady=(10, 0), sticky="ew")

        submit_button = ctk.CTkButton(
            self.enter_code_frame,
            text="Submit",
            font=ctk.CTkFont(size=14, weight="bold"),
            command=self.on_submit_code_click,
        )
        submit_button.grid(row=5, column=0, padx=10, pady=(20, 0), sticky="ew")

        self.resend_label = ctk.CTkLabel(
            self.enter_code_frame,
            text="Resend Email",
            text_color="blue",
            cursor="hand2",
            font=ctk.CTkFont(size=14),
        )
        self.resend_label.grid(row=6, column=0, padx=10, pady=(10, 0), sticky="ew")
        self.resend_label.bind("<Button-1>", lambda e: self.resend_verification_code())

    def create_reset_password_frame(self) -> None:
        self.reset_password_frame = ctk.CTkFrame(
            self.forgot_password_center_frame, fg_color="#F1F2F3"
        )
        self.reset_password_frame.grid(row=1, column=1, pady=(20, 20), sticky="nsew")
        configure_grid(self.reset_password_frame, rows=8, columns=0)

        title = ctk.CTkLabel(
            self.reset_password_frame,
            text="Reset your password",
            font=ctk.CTkFont(size=24, weight="bold"),
        )
        title.grid(row=0, column=0, padx=10, pady=(10, 20), sticky="nsew")

        password_label = ctk.CTkLabel(
            self.reset_password_frame, text="Enter Password:", font=ctk.CTkFont(size=14)
        )
        password_label.grid(row=1, column=0, padx=(13, 0), pady=(15, 0), sticky="sw")

        password_info_label = ctk.CTkLabel(
            self.reset_password_frame, text="", image=self.icon_info
        )
        password_info_label.grid(
            row=1, column=0, padx=(0, 15), pady=(15, 0), sticky="se"
        )

        Tooltip(
            password_info_label,
            text="Length at least 8 characters\n"
            "At least one uppercase letter\n"
            "At least one lowercase letter\n"
            "At least one number\n"
            "At least one special character",
            hover_delay=175,
        )

        self.password_entry_forgot_password = ctk.CTkEntry(
            self.reset_password_frame, show="*", placeholder_text="*****"
        )
        self.password_entry_forgot_password.grid(row=2, column=0, padx=10, sticky="new")

        confirm_password_label = ctk.CTkLabel(
            self.reset_password_frame,
            text="Re-enter Password:",
            font=ctk.CTkFont(size=14),
        )
        confirm_password_label.grid(
            row=3, column=0, padx=(13, 0), pady=(15, 0), sticky="sw"
        )

        self.confirm_password_entry_forgot_password = ctk.CTkEntry(
            self.reset_password_frame, show="*", placeholder_text="*****"
        )
        self.confirm_password_entry_forgot_password.grid(
            row=4, column=0, padx=10, sticky="new"
        )

        self.error_label_password = ctk.CTkLabel(
            self.reset_password_frame,
            text="",
            text_color="red",
            font=ctk.CTkFont(size=12),
        )
        self.error_label_password.grid(
            row=5, column=0, padx=10, pady=(5, 0), sticky="nw"
        )

        reset_button = ctk.CTkButton(
            self.reset_password_frame,
            text="Reset Password",
            font=ctk.CTkFont(size=14, weight="bold"),
            command=self.on_reset_password,
        )
        reset_button.grid(row=6, column=0, padx=10, pady=(20, 0), sticky="ew")

    def on_send_code_click(self) -> None:
        email = self.email_entry_forgot_password.get().strip()
        self.error_label.configure(text="")

        if not email or not self.auth.is_email_taken(email):
            self.error_label.configure(
                text="This email is not associated with any account."
            )
            return

        if request_verification_code(email):
            self.enter_code_frame.tkraise()
            self.start_timer()

    def on_submit_code_click(self) -> None:
        email = self.email_entry_forgot_password.get().strip()
        code = self.code_entry.get().strip()
        self.error_label_otp.configure(text="")

        if not code:
            self.error_label_otp.configure(text="Please enter the verification code.")
            return

        if request_verify_otp(email, code):
            print("Success", "Verification successful!")
            self.reset_password_frame.tkraise()
        else:
            self.error_label_otp.configure(
                text="Invalid verification code. Please try again."
            )

    def on_reset_password(self) -> None:
        password = self.password_entry_forgot_password.get().strip()
        confirm_password = self.confirm_password_entry_forgot_password.get().strip()
        self.error_label_password.configure(text="")

        if not re.match(
            r"^(?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*[!@#$%^&*()_+=\{\[\]\\|:;'<>/?~]).{8,}$",
            password,
        ):
            self.error_label_password.configure(
                text="Password does not meet requirements."
            )
            return

        if password != confirm_password:
            self.error_label_password.configure(text="Passwords do not match.")
            return

        if self.auth.update_password(self.email_entry_forgot_password.get(), password):
            print("Success", "Password has been updated successfully!")
            self.forgot_password_window.destroy()
        else:
            print("Failed to update password.")

    def resend_verification_code(self) -> None:
        self.send_code_frame.tkraise()
        self.start_timer()

    def start_timer(self) -> None:
        self.time_left = 60
        self.resend_label.configure(text_color="grey", cursor="arrow")
        self.resend_label.unbind("<Button-1>")
        self.update_timer()

    def update_timer(self) -> None:
        if self.timer:
            self.timer.cancel()

        if self.time_left > 0:
            self.timer_label.configure(text=f"Code expires in {self.time_left} seconds")
            self.time_left -= 1
            self.timer = threading.Timer(1.0, self.update_timer)
            self.timer.start()
        else:
            self.timer_label.configure(
                text="Code has expired. Resend email to get a new code."
            )
            self.resend_label.configure(text_color="blue", cursor="hand2")
            self.resend_label.bind(
                "<Button-1>", lambda e: self.resend_verification_code()
            )
