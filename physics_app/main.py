import tkinter as tk

import customtkinter as ctk

from physics_app.modules.user_authentication import UserAuthentication
from physics_app.views.signUp_login_page import SignUpLoginPage


class PhysicsApp(tk.Frame):
    def __init__(self, master: tk.Tk = None):
        super().__init__(master)
        self.master = master
        self.auth = UserAuthentication("../data/physics_revision_app.db")
        self.create_widgets()

    def create_widgets(self):
        self.signUp_login_page = SignUpLoginPage(self, self.auth)
        self.signUp_login_page.grid(row=0, column=0)


def main():
    root = ctk.CTk()
    app = PhysicsApp(master=root)
    root.title("Physics App")
    root.state("zoomed")
    app.pack(fill=tk.BOTH, expand=True)
    root.mainloop()


if __name__ == "__main__":
    main()
