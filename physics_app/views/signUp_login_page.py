import tkinter as tk
import customtkinter as ctk
from PIL import Image, ImageTk
from physics_app.modules.user_authentication import UserAuthentication


class SignUpLoginPage(tk.Frame):
    def __init__(self, master, auth: UserAuthentication):
        super().__init__(master)
        self.master = master
        self.auth = auth
        self.configure(bg="white")
        self.pack(fill=tk.BOTH, expand=True)
        self.create_widgets()

    def create_widgets(self):
        self.setup_appearance()
        self.setup_center_frame()
        self.setup_canvas()
        self.setup_content_frame()
        self.create_sign_up_widgets()
        self.create_login_widgets()
        self.sign_up_frame.tkraise()

    def setup_appearance(self):
        ctk.set_appearance_mode("light")
        ctk.set_default_color_theme("blue")

    def setup_center_frame(self):
        self.center_frame = ctk.CTkFrame(self.master, fg_color="white")
        self.center_frame.pack(expand=True, fill=tk.BOTH, anchor="center")
        self.center_frame.grid_rowconfigure(0, weight=0)
        self.center_frame.grid_rowconfigure(1, weight=1)
        self.center_frame.grid_columnconfigure(0, weight=1)
        self.center_frame.grid_columnconfigure(1, weight=1)
        self.center_frame.grid_columnconfigure(2, weight=1)

    def setup_canvas(self):
        self.canvas_for_image = ctk.CTkCanvas(
            self.center_frame, borderwidth=0, highlightthickness=0, bg="white"
        )
        self.canvas_for_image.grid(row=0, column=1, sticky="nsew")
        self.image = Image.open("assets/physics_logo.png")
        self.canvas_for_image.bind("<Configure>", self.resize_image)

    def setup_content_frame(self):
        self.content_frame = ctk.CTkFrame(self.center_frame, fg_color="white")
        self.content_frame.grid(row=1, column=1, sticky="nsew")
        self.content_frame.grid_columnconfigure(0, weight=1)
        self.content_frame.grid_columnconfigure(1, weight=1)
        self.content_frame.grid_columnconfigure(2, weight=1)
        self.content_frame.grid_propagate(False)
        self.content_frame.configure(height=400)

    def create_sign_up_widgets(self):
        self.sign_up_frame = ctk.CTkFrame(self.content_frame, fg_color="#F1F2F3")
        self.sign_up_frame.grid(row=0, column=1, sticky="n")

        self.configure_grid(self.sign_up_frame, rows=10, columns=3)

        title = ctk.CTkLabel(
            self.sign_up_frame, text="Sign Up", font=ctk.CTkFont(size=20, weight="bold")
        )
        title.grid(row=0, column=1, pady=(10, 20), sticky="nsew")

        email_label = ctk.CTkLabel(
            self.sign_up_frame, text="Email:", font=ctk.CTkFont(size=14)
        )
        email_label.grid(row=1, column=1, padx=(15, 0), sticky="sw")
        self.email_entry_sign_up = ctk.CTkEntry(
            self.sign_up_frame, placeholder_text="user@email.com"
        )
        self.email_entry_sign_up.grid(row=2, column=1, padx=10, sticky="new")

        username_label = ctk.CTkLabel(
            self.sign_up_frame, text="Username:", font=ctk.CTkFont(size=14)
        )
        username_label.grid(row=3, column=1, padx=(15, 0), pady=(15, 0), sticky="sw")
        self.username_entry_sign_up = ctk.CTkEntry(
            self.sign_up_frame, placeholder_text="username"
        )
        self.username_entry_sign_up.grid(row=4, column=1, padx=10, sticky="new")

        password_label = ctk.CTkLabel(
            self.sign_up_frame, text="Password:", font=ctk.CTkFont(size=14)
        )
        password_label.grid(row=5, column=1, padx=(15, 0), pady=(15, 0), sticky="sw")
        self.password_entry_sign_up = ctk.CTkEntry(
            self.sign_up_frame, show="*", placeholder_text="*****"
        )
        self.password_entry_sign_up.grid(row=6, column=1, padx=10, sticky="new")

        signup_button = ctk.CTkButton(
            self.sign_up_frame,
            text="Sign Up",
            font=ctk.CTkFont(size=14),
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
        self.login_frame.grid(row=0, column=1, sticky="n")

        self.configure_grid(self.login_frame, rows=4, columns=3)

        title = ctk.CTkLabel(
            self.login_frame, text="Log In", font=ctk.CTkFont(size=20, weight="bold")
        )
        title.grid(row=0, column=1, padx=10, pady=(10, 20), sticky="nsew")

        username_label = ctk.CTkLabel(
            self.login_frame, text="Email:", font=ctk.CTkFont(size=14)
        )
        username_label.grid(row=1, column=1, padx=(15, 0), sticky="sw")
        self.username_entry_login = ctk.CTkEntry(
            self.login_frame, placeholder_text="Enter your email or username"
        )
        self.username_entry_login.grid(row=2, column=1, padx=10, sticky="new")

        password_label = ctk.CTkLabel(
            self.login_frame, text="Password:", font=ctk.CTkFont(size=14)
        )
        password_label.grid(row=3, column=1, padx=(15, 0), pady=(15, 0), sticky="sw")
        forgot_password_label = ctk.CTkLabel(
            self.login_frame,
            text="Forgot password?",
            text_color="blue",
            cursor="hand2",
            font=ctk.CTkFont(size=14),
        )
        forgot_password_label.grid(row=3, column=1, padx=10, pady=(15, 0), sticky="se")
        self.password_entry_login = ctk.CTkEntry(
            self.login_frame, show="*", placeholder_text="*****"
        )
        self.password_entry_login.grid(row=4, column=1, padx=10, sticky="new")

        login_button = ctk.CTkButton(
            self.login_frame,
            text="Log In",
            font=ctk.CTkFont(size=14),
            command=self.login_user,
        )
        login_button.grid(row=5, column=1, padx=10, pady=(20, 0), sticky="ew")

        signup_label = ctk.CTkLabel(
            self.login_frame,
            text="Don't have an account? Sign up",
            text_color="blue",
            cursor="hand2",
            font=ctk.CTkFont(size=14),
        )
        signup_label.grid(row=6, column=1, padx=10, pady=(8, 0), sticky="ew")
        signup_label.bind("<Button-1>", lambda e: self.show_frame(self.sign_up_frame))

    def configure_grid(self, frame, rows, columns):
        for i in range(columns):
            frame.grid_columnconfigure(i, weight=1)
        for i in range(1, rows):
            frame.grid_rowconfigure(i, weight=1)

    def register_user(self):
        email = self.email_entry_sign_up.get()
        username = self.username_entry_sign_up.get()
        password = self.password_entry_sign_up.get()
        print(f"Email: {email}, Username: {username}, Password: {password}")
        self.auth.insert_user_into_db(email, username, password)

    def login_user(self):
        email_username = self.username_entry_login.get()
        password = self.password_entry_login.get()
        self.auth.confirm_user_details(email_username, password)

    def show_frame(self, frame):
        self.clear_entries()
        if frame == self.sign_up_frame:
            self.login_frame.grid_forget()
            self.sign_up_frame.grid(row=1, column=1, padx=10, sticky="n")
            self.sign_up_frame.tkraise()
        else:
            self.sign_up_frame.grid_forget()
            self.login_frame.grid(row=1, column=1, padx=10, sticky="n")
            self.login_frame.tkraise()

    def clear_entries(self):
        entries = [
            (self.email_entry_sign_up, "user@email.com"),
            (self.username_entry_sign_up, "username"),
            (self.password_entry_sign_up, "*****"),
            (self.username_entry_login, "Enter your email or username"),
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
