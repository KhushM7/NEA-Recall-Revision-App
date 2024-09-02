import tkinter as tk
import customtkinter as ctk

from physics_app.views.Sign_Up_Login_DIR.sign_up_login_page import SignUpLoginPage
from physics_app.views.home_page import HomePage


class PhysicsApp(tk.Frame):
    def __init__(self, master: tk.Tk = None):
        super().__init__(master)
        self.master = master
        self.server_url = "http://127.0.0.1:5000"
        self.create_widgets()

    def create_widgets(self):
        # Initialize the sign-up/login page
        self.sign_up_login_page = SignUpLoginPage(self, self.server_url)
        self.sign_up_login_page.grid(row=0, column=0, sticky="nsew")

        # Initialize the home page
        self.home_page = HomePage(self, self.server_url)

    def show_home_page(self):
        # Hide the sign-up/login page and show the home page
        self.sign_up_login_page.grid_forget()
        self.home_page.grid(row=0, column=0, sticky="nsew")


def main():
    # Set up the main application window
    root = ctk.CTk()
    app = PhysicsApp(master=root)
    app.grid(row=0, column=0, sticky="nsew")
    root.title("Physics App")

    # Make the grid expandable
    root.grid_rowconfigure(0, weight=1)
    root.grid_columnconfigure(0, weight=1)

    # Set the window size to fullscreen
    width, height = root.winfo_screenwidth(), root.winfo_screenheight()
    root.geometry(f"{width}x{height}")

    # Start the application main loop
    root.mainloop()


if __name__ == "__main__":
    main()
