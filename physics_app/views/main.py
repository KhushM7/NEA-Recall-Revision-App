import tkinter as tk
import customtkinter as ctk

from physics_app.views.Sign_Up_Login.sign_up_login_page import SignUpLoginPage
from physics_app.views.create_set_page import CreateSetPage
from physics_app.views.flashcard_reviewer import FlashcardReviewer
from physics_app.views.home_page import HomePage


class PhysicsApp(tk.Frame):
    def __init__(self, master: tk.Tk = None):
        super().__init__(master)
        self.master = master
        self.server_url = "http://127.0.0.1:5000"
        self.user_id = 0
        self.show_login_page()
        self.master.grid_rowconfigure(0, weight=1)
        # self.master.grid_rowconfigure(1, weight=0)
        # self.master.grid_rowconfigure(2, weight=0)
        self.master.grid_columnconfigure(0, weight=1)
        # self.master.grid_columnconfigure(1, weight=0)
        # self.master.grid_columnconfigure(2, weight=0)

    def show_login_page(self):
        """Displays the sign-up/login page."""
        # Clear any existing widgets
        for widget in self.winfo_children():
            widget.destroy()

        # Initialize the SignUpLoginPage with callback to `show_home_page`
        self.sign_up_login_page = SignUpLoginPage(
            self, self.server_url, self.handle_login_success
        )
        self.sign_up_login_page.grid(row=0, column=0, sticky="nsew")

    def handle_login_success(self, user_id):
        """
        Callback function to handle successful login.
        Sets user_id and transitions to the home page.
        """
        self.user_id = user_id
        self.show_home_page()

    def show_home_page(self):
        """Clears the frame and displays the home page."""
        for widget in self.winfo_children():
            widget.destroy()
        # Initialize HomePage with a button to start reviewing flashcards
        self.home_page = HomePage(
            self,
            self.user_id,
            self.server_url,
            lambda review_type: self.show_flashcard_reviewer(self.user_id, review_type),
            lambda: self.on_create_set_click(self.user_id),
        )

        self.home_page.grid(row=0, column=1, sticky="nsew")

    def on_create_set_click(self, user_id):
        """Callback function to handle the create set button click."""
        for widget in self.winfo_children():
            widget.destroy()
        self.create_set_page = CreateSetPage(self, user_id, self.show_home_page)
        # self.grid_rowconfigure(0, weight=1)
        # self.grid_rowconfigure(1, weight=1)
        # self.grid_rowconfigure(2, weight=1)
        # self.grid_columnconfigure(0, weight=1)
        # self.grid_columnconfigure(1, weight=1)
        # self.grid_columnconfigure(2, weight=1)
        self.create_set_page.grid(row=0, column=0, sticky="nsew")

    def show_flashcard_reviewer(self, user_id, review_type):
        """Clears the frame and displays the flashcard reviewer page."""
        for widget in self.winfo_children():
            widget.destroy()

        # Initialize FlashcardReviewer with `on_close` callback to return to home page
        self.flashcard_reviewer = FlashcardReviewer(
            self, user_id, self.show_home_page, review_type
        )
        # self.grid_rowconfigure(0, weight=1)
        # self.grid_rowconfigure(1, weight=1)
        # self.grid_rowconfigure(2, weight=1)
        # self.grid_columnconfigure(0, weight=1)
        # self.grid_columnconfigure(1, weight=1)
        # self.grid_columnconfigure(2, weight=1)
        self.flashcard_reviewer.grid(row=0, column=0, sticky="nsew")


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
