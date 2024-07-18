import tkinter as tk
import customtkinter as ctk
from PIL import Image
from physics_app.modules.user_authentication import UserAuthentication


class SignUpLoginPage(tk.Frame):
    def __init__(self, master, auth: UserAuthentication):
        super().__init__(master)
        self.master = master
        master.grid_rowconfigure(index=0, weight=1)
        master.grid_columnconfigure(index=0, weight=1)
        master.grid_columnconfigure(index=1, weight=1)
        self.grid(row=0, column=0, sticky=tk.N + tk.S + tk.E + tk.W)
        self.auth = auth
        self.create_widgets()

    def create_widgets(self):
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        left_frame = ctk.CTkFrame(self.master, width=400, height=400)
        left_frame.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")
        physics_logo = ctk.CTkImage(
            light_image=Image.open("assets/physics_logo.png"),
            size=(400, 400),
        )
        physics_logo_label = ctk.CTkLabel(left_frame, image=physics_logo, text="")
        physics_logo_label.grid(row=0, column=0, pady=(10, 20), sticky="nsew")
        left_frame.grid_rowconfigure(1, weight=1)

        right_frame = ctk.CTkFrame(self.master, width=400, height=400)
        right_frame.grid(row=0, column=1, padx=20, pady=20, sticky="nsew")
        right_frame.grid_rowconfigure(0, weight=1)
        right_frame.grid_rowconfigure(1, weight=1)
        right_frame.grid_rowconfigure(2, weight=1)
        right_frame.grid_rowconfigure(3, weight=1)
        right_frame.grid_rowconfigure(4, weight=1)
        right_frame.grid_rowconfigure(5, weight=1)
        right_frame.grid_rowconfigure(6, weight=1)
        right_frame.grid_rowconfigure(7, weight=1)
        right_frame.grid_rowconfigure(8, weight=1)
        right_frame.grid_columnconfigure(0, weight=1)

        title = ctk.CTkLabel(
            right_frame,
            text="Sign up",
            font=ctk.CTkFont(size=20, weight="bold"),
        )
        title.grid(row=0, column=0, pady=(10, 20), sticky="nsew")

        email_label = ctk.CTkLabel(right_frame, text="Email")
        email_label.grid(row=1, column=0, pady=(5, 0), sticky="nsew")
        email_entry = ctk.CTkEntry(right_frame, placeholder_text="user@email.com")
        email_entry.grid(row=2, column=0, pady=(0, 5), sticky="nsew")

        username_label = ctk.CTkLabel(right_frame, text="Username")
        username_label.grid(row=3, column=0, pady=(5, 0), sticky="nsew")
        username_entry = ctk.CTkEntry(right_frame, placeholder_text="username")
        username_entry.grid(row=4, column=0, pady=(0, 5), sticky="nsew")

        password_label = ctk.CTkLabel(right_frame, text="Password")
        password_label.grid(row=5, column=0, pady=(5, 0), sticky="nsew")
        password_entry = ctk.CTkEntry(right_frame, show="*", placeholder_text="*****")
        password_entry.grid(row=6, column=0, pady=(0, 5), sticky="nsew")

        signup_button = ctk.CTkButton(right_frame, text="Sign up")
        signup_button.grid(row=8, column=0, pady=(20, 5), sticky="nsew")

        login_label = ctk.CTkLabel(right_frame, text="Already have an account? Log in")
        login_label.grid(row=9, column=0, pady=(5, 10), sticky="nsew")
