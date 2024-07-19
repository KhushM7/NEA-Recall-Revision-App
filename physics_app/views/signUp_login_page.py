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
        center_frame.grid_rowconfigure(0, weight=0)
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

        notebook_frame = ctk.CTkFrame(center_frame, fg_color="white")
        notebook_frame.grid(row=1, column=0, sticky="nsew", padx=20, pady=20)
        notebook_frame.grid_rowconfigure(0, weight=1)
        notebook_frame.grid_rowconfigure(1, weight=1)
        notebook_frame.grid_columnconfigure(0, weight=1)
        notebook_frame.grid_columnconfigure(1, weight=1)
        notebook_frame.grid_columnconfigure(2, weight=1)

        self.tab_view = ctk.CTkTabview(notebook_frame, fg_color="#F1F2F3")
        self.tab_view.grid(row=0, column=1, sticky="nsew")
        self.tab_view.grid_propagate(False)

        self.sign_up_tab = self.tab_view.add(name="Sign Up")
        self.sign_up_frame = ctk.CTkFrame(self.sign_up_tab, fg_color="#F1F2F3")
        self.sign_up_frame.grid(row=0, column=1, sticky="nsew")
        self.tab_view.grid_propagate(False)
        self.sign_up_tab.grid_rowconfigure(0, weight=1)
        self.sign_up_tab.grid_columnconfigure(0, weight=1)
        self.create_sign_up_widgets()

        self.login_tab = self.tab_view.add("Log In")
        self.login_frame = ctk.CTkFrame(self.login_tab, fg_color="#F1F2F3")
        self.login_frame.grid(row=0, column=1, sticky="nsew")
        self.tab_view.grid_propagate(False)
        self.login_tab.grid_rowconfigure(0, weight=1)
        self.login_tab.grid_columnconfigure(0, weight=1)
        self.create_login_widgets()

    def create_sign_up_widgets(self):
        for i in range(3):
            self.sign_up_frame.grid_columnconfigure(i, weight=1)
        for i in range(1, 10):
            self.sign_up_frame.grid_rowconfigure(i, weight=1)
        self.sign_up_frame.grid(row=0, column=0, sticky="nsew")

        self.sign_up_frame.grid_rowconfigure(index=0, weight=0)
        title = ctk.CTkLabel(
            self.sign_up_frame, text="Sign Up", font=ctk.CTkFont(size=20, weight="bold")
        )
        title.grid(row=0, column=1, pady=(10, 20), sticky="nsew")

        email_label = ctk.CTkLabel(self.sign_up_frame, text="Email")
        email_label.grid(row=1, column=1, sticky="sw")
        email_entry = ctk.CTkEntry(
            self.sign_up_frame, placeholder_text="user@email.com"
        )
        email_entry.grid(row=2, column=1, sticky="new")

        username_label = ctk.CTkLabel(self.sign_up_frame, text="Username")
        username_label.grid(row=3, column=1, sticky="sw")
        username_entry = ctk.CTkEntry(self.sign_up_frame, placeholder_text="username")
        username_entry.grid(row=4, column=1, sticky="new")

        password_label = ctk.CTkLabel(self.sign_up_frame, text="Password")
        password_label.grid(row=5, column=1, sticky="sw")
        password_entry = ctk.CTkEntry(
            self.sign_up_frame, show="*", placeholder_text="*****"
        )
        password_entry.grid(row=6, column=1, sticky="new")

        # self.sign_up_frame.grid_rowconfigure(index=8, weight=0)
        signup_button = ctk.CTkButton(self.sign_up_frame, text="Sign Up")
        signup_button.grid(row=8, column=1, sticky="ew")

        # self.sign_up_frame.grid_rowconfigure(index=9, weight=0)
        login_label = ctk.CTkLabel(
            self.sign_up_frame,
            text="Already have an account? Log in",
            text_color="blue",
            cursor="hand2",
        )
        login_label.grid(row=9, column=1, sticky="ew")
        login_label.bind("<Button-1>", lambda e: self.show_frame("Log In"))

    def create_login_widgets(self):
        for i in range(3):
            self.login_frame.grid_columnconfigure(i, weight=1)
        for i in range(1, 7):
            self.login_frame.grid_rowconfigure(i, weight=1)
        self.login_frame.grid(row=0, column=0, sticky="nsew")

        self.login_frame.grid_rowconfigure(index=0, weight=0)
        title = ctk.CTkLabel(
            self.login_frame, text="Log In", font=ctk.CTkFont(size=20, weight="bold")
        )
        title.grid(row=0, column=1, pady=(10, 20), sticky="nsew")

        username_label = ctk.CTkLabel(self.login_frame, text="Username")
        username_label.grid(row=1, column=1, sticky="sw")
        username_entry = ctk.CTkEntry(self.login_frame, placeholder_text="username")
        username_entry.grid(row=2, column=1, sticky="new")

        password_label = ctk.CTkLabel(self.login_frame, text="Password")
        password_label.grid(row=3, column=1, sticky="sw")
        forgot_password_label = ctk.CTkLabel(self.login_frame, text="Forgot password?")
        forgot_password_label.grid(row=3, column=1, sticky="se")
        password_entry = ctk.CTkEntry(
            self.login_frame, show="*", placeholder_text="*****"
        )
        password_entry.grid(row=4, column=1, sticky="new")

        # self.login_frame.grid_rowconfigure(index=5, weight=0)
        login_button = ctk.CTkButton(self.login_frame, text="Log In")
        login_button.grid(row=5, column=1, sticky="ew")

        # self.login_frame.grid_rowconfigure(index=6, weight=0)
        signup_label = ctk.CTkLabel(
            self.login_frame,
            text="Don't have an account? Sign up",
            text_color="blue",
            cursor="hand2",
        )
        signup_label.grid(row=6, column=1, sticky="ew")
        signup_label.bind("<Button-1>", lambda e: self.show_frame("Sign Up"))

    def show_frame(self, tab_name):
        self.tab_view.set(tab_name)
