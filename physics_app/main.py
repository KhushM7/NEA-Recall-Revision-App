import tkinter as tk
import sv_ttk
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
        self.signUp_login_page.pack()


def main():
    root = tk.Tk()
    app = PhysicsApp(master=root)
    root.title("Physics App")
    root.state("zoomed")
    sv_ttk.use_light_theme()
    app.pack(expand=True, fill="both")
    root.mainloop()


if __name__ == "__main__":
    main()
