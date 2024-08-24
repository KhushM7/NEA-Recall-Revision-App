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
        # Initialize and pack the sign-up/login page
        self.sign_up_login_page = SignUpLoginPage(self, self.server_url)
        self.sign_up_login_page.pack(fill=tk.BOTH, expand=True)

        self.home_page = HomePage(self, self.server_url)
        self.home_page.pack(fill=tk.BOTH, expand=True)


def main():
    # Set up the main application window
    root = ctk.CTk()
    app = PhysicsApp(master=root)
    app.pack(fill=tk.BOTH, expand=True)
    root.title("Physics App")

    # Set the window size to fullscreen
    width, height = root.winfo_screenwidth(), root.winfo_screenheight()
    root.geometry(f"{width}x{height}")

    # Start the application main loop
    root.mainloop()


if __name__ == "__main__":
    main()
