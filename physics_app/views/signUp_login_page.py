import tkinter as tk
import customtkinter as ctk
from PIL import Image, ImageTk
from ctypes import windll
from physics_app.modules.user_authentication import UserAuthentication
from physics_app.utilities.utilities import make_widget_transparent


class SignUpLoginPage(tk.Frame):
    def __init__(self, master, auth: UserAuthentication):
        super().__init__(master)
        self.master = master
        self.master.grid_rowconfigure(index=0, weight=1)
        self.master.grid_columnconfigure(index=0, weight=1)
        self.master.grid_columnconfigure(index=1, weight=1)
        self.master.grid_columnconfigure(index=2, weight=1)
        self.grid(row=0, column=0, sticky=tk.N + tk.S + tk.E + tk.W)
        self.auth = auth
        self.create_widgets()

    def create_widgets(self):
        ctk.set_appearance_mode("light")
        ctk.set_default_color_theme("blue")

        center_frame = ctk.CTkFrame(self.master, fg_color="white")
        center_frame.grid(row=0, column=1, padx=20, pady=20, sticky="nsew")
        center_frame.grid_rowconfigure(0, weight=1)
        center_frame.grid_rowconfigure(1, weight=1)
        center_frame.grid_columnconfigure(0, weight=1)

        canvas_for_image = ctk.CTkCanvas(
            center_frame,
            height=150,
            width=850,
            borderwidth=0,
            highlightthickness=0,
            bg="white",
        )
        canvas_for_image.grid(row=0, column=0, sticky="n", padx=0, pady=60)

        image = Image.open("assets/physics_logo.png")
        new_width = 850
        aspect_ratio = image.height / image.width
        new_height = int(new_width * aspect_ratio)
        canvas_for_image.image = ImageTk.PhotoImage(
            image.resize((new_width, new_height), Image.Resampling.LANCZOS)
        )

        def place_image():
            canvas_center_x = int(canvas_for_image.winfo_width() / 2)
            canvas_center_y = int(canvas_for_image.winfo_height() / 2)
            canvas_for_image.create_image(
                canvas_center_x,
                canvas_center_y,
                image=canvas_for_image.image,
                anchor="center",
            )

        canvas_for_image.after(100, place_image)
        self.master.after(10, lambda: make_widget_transparent(canvas_for_image))

        notebook = ctk.CTkFrame(center_frame)
        notebook.grid(row=1, column=0, sticky="nsew", padx=20, pady=20)
        notebook.grid_rowconfigure(0, weight=1)
        notebook.grid_columnconfigure(0, weight=1)

        self.tab_control = ctk.CTkFrame(notebook)
        self.tab_control.grid(row=0, column=0, sticky="nsew")
        self.tab_control.grid_rowconfigure(0, weight=1)
        self.tab_control.grid_columnconfigure(0, weight=1)

        # Sign Up tab
        self.sign_up_frame = ctk.CTkFrame(self.tab_control)
        self.sign_up_frame.grid(row=0, column=0, sticky="nsew")
        self.create_sign_up_widgets()

        # Login tab
        self.login_frame = ctk.CTkFrame(self.tab_control)
        self.login_frame.grid(row=0, column=0, sticky="nsew")
        self.create_login_widgets()

        self.show_frame(self.sign_up_frame)

        # Tabs
        tab_frame = ctk.CTkFrame(center_frame)
        tab_frame.grid(row=2, column=0, sticky="ew", padx=20, pady=(0, 20))
        tab_frame.grid_columnconfigure(0, weight=1)
        tab_frame.grid_columnconfigure(1, weight=1)

        sign_up_tab = ctk.CTkButton(
            tab_frame,
            text="Sign Up",
            command=lambda: self.show_frame(self.sign_up_frame),
        )
        sign_up_tab.grid(row=0, column=0, sticky="ew")

        login_tab = ctk.CTkButton(
            tab_frame, text="Log In", command=lambda: self.show_frame(self.login_frame)
        )
        login_tab.grid(row=0, column=1, sticky="ew")

    def show_frame(self, frame):
        frame.tkraise()

    def create_sign_up_widgets(self):
        self.sign_up_frame.grid(row=0, column=0, sticky="nsew")

        title = ctk.CTkLabel(
            self.sign_up_frame, text="Sign Up", font=ctk.CTkFont(size=20, weight="bold")
        )
        title.grid(row=0, column=0, pady=(10, 20), sticky="nsew")

        email_label = ctk.CTkLabel(self.sign_up_frame, text="Email")
        email_label.grid(row=1, column=0, pady=(5, 0), sticky="nsew")
        email_entry = ctk.CTkEntry(
            self.sign_up_frame, placeholder_text="user@email.com"
        )
        email_entry.grid(row=2, column=0, pady=(0, 5), sticky="nsew")

        username_label = ctk.CTkLabel(self.sign_up_frame, text="Username")
        username_label.grid(row=3, column=0, pady=(5, 0), sticky="nsew")
        username_entry = ctk.CTkEntry(self.sign_up_frame, placeholder_text="username")
        username_entry.grid(row=4, column=0, pady=(0, 5), sticky="nsew")

        password_label = ctk.CTkLabel(self.sign_up_frame, text="Password")
        password_label.grid(row=5, column=0, pady=(5, 0), sticky="nsew")
        password_entry = ctk.CTkEntry(
            self.sign_up_frame, show="*", placeholder_text="*****"
        )
        password_entry.grid(row=6, column=0, pady=(0, 5), sticky="nsew")

        signup_button = ctk.CTkButton(self.sign_up_frame, text="Sign Up")
        signup_button.grid(row=8, column=0, pady=(20, 5), sticky="nsew")

        login_label = ctk.CTkLabel(
            self.sign_up_frame, text="Already have an account? Log in"
        )
        login_label.grid(row=9, column=0, pady=(5, 10), sticky="nsew")

    def create_login_widgets(self):
        self.login_frame.grid(row=0, column=0, sticky="nsew")

        title = ctk.CTkLabel(
            self.login_frame, text="Log In", font=ctk.CTkFont(size=20, weight="bold")
        )
        title.grid(row=0, column=0, pady=(10, 20), sticky="nsew")

        username_label = ctk.CTkLabel(self.login_frame, text="Username")
        username_label.grid(row=1, column=0, pady=(5, 0), sticky="nsew")
        username_entry = ctk.CTkEntry(self.login_frame, placeholder_text="username")
        username_entry.grid(row=2, column=0, pady=(0, 5), sticky="nsew")

        password_label = ctk.CTkLabel(self.login_frame, text="Password")
        password_label.grid(row=3, column=0, pady=(5, 0), sticky="nsew")
        password_entry = ctk.CTkEntry(
            self.login_frame, show="*", placeholder_text="*****"
        )
        password_entry.grid(row=4, column=0, pady=(0, 5), sticky="nsew")

        login_button = ctk.CTkButton(self.login_frame, text="Log In")
        login_button.grid(row=5, column=0, pady=(20, 5), sticky="nsew")

        signup_label = ctk.CTkLabel(
            self.login_frame, text="Don't have an account? Sign up"
        )
        signup_label.grid(row=6, column=0, pady=(5, 10), sticky="nsew")
