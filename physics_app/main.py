import tkinter as tk

import customtkinter as ctk

from physics_app.views.signUp_login_page import SignUpLoginPage
from physics_app.modules.user_authentication import UserAuthentication


class PhysicsApp(tk.Frame):
    def __init__(self, master: tk.Tk = None):
        super().__init__(master)
        self.master = master
        self.auth = UserAuthentication(
            "C:\\Users\\khush\\PycharmProjects\\NEA-Physics-Revision-App\\data\\physics_revision_app.db"
        )
        self.create_widgets()

    def create_widgets(self):
        self.signUp_login_page = SignUpLoginPage(self, self.auth)
        self.pack()
        return


def main():
    root = ctk.CTk()
    app = PhysicsApp(master=root)
    app.pack(fill=tk.BOTH, expand=True)
    root.title("Physics App")
    width = root.winfo_screenwidth()
    height = root.winfo_screenheight()
    tam = "%dx%d" % (width, height)
    root.geometry(tam)
    root.mainloop()


if __name__ == "__main__":
    main()
