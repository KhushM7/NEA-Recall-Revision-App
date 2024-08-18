import tkinter as tk
import customtkinter as ctk

from physics_app.views.Sign_Up_Login_DIR.sign_up_login_page import SignUpLoginPage
from physics_app.modules.user_authentication import UserAuthentication


class PhysicsApp(tk.Frame):
    def __init__(self, master: tk.Tk = None):
        super().__init__(master)
        self.master = master
        self.auth = UserAuthentication("data/physics_revision_app.db")
        self.create_widgets()

    def create_widgets(self):
        # Initialize and pack the sign-up/login page
        self.sign_up_login_page = SignUpLoginPage(self, self.auth)
        self.pack(fill=tk.BOTH, expand=True)


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
