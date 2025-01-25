import tkinter as tk
import customtkinter as ctk

from physics_app.views.Sign_Up_Login.sign_up_login_page import SignUpLoginPage
from physics_app.views.create_set_page import CreateSetPage
from physics_app.views.flashcard_reviewer import (
    ScheduledFlashcardReviewer,
    UnscheduledFlashcardReviewer,
)
from physics_app.views.home_page import HomePage
from physics_app.views.library_page import LibraryPage


class PhysicsApp(tk.Frame):
    def __init__(self, master: tk.Tk = None):
        """
        Main application frame that stacks pages and dynamically shows them.
        """
        super().__init__(master)
        self.master = master
        self.server_url = "http://127.0.0.1:5000"
        self.user_id = 0

        # Configure grid to expand for the container
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # Container to hold all pages
        self.container = ctk.CTkFrame(self)
        self.container.grid(row=0, column=0, sticky="nsew")
        self.container.grid(row=0, column=0, sticky="nsew")
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_rowconfigure(1, weight=1)
        self.container.grid_rowconfigure(2, weight=1)
        self.container.grid_columnconfigure(0, weight=1)
        self.container.grid_columnconfigure(1, weight=1)
        self.container.grid_columnconfigure(2, weight=1)

        # Dictionary to hold references to active frames
        self.frames = {}

        # Start with login page
        self.show_login_page()

    def show_frame(self, row, col, frame_class, *args):
        """
        Displays the requested frame, dynamically initializing it if not created yet.
        Args:
            frame_class: The class of the frame to be shown.
            row: The row to place the frame in.
            col: The column to place the frame in.
            *args: Arguments to pass when creating the frame.
        """

        # Clear any existing frame
        for frame in self.container.winfo_children():
            frame.destroy()

        # Create the requested frame
        frame = frame_class(self.container, *args)
        frame.grid(row=row, column=col, sticky="nsew")

    def show_login_page(self):
        """Displays the login page."""
        self.show_frame(
            0, 0, SignUpLoginPage, self.server_url, self.handle_login_success
        )

    def handle_login_success(self, user_id):
        """
        Callback function after successful login.
        Args:
            user_id: The ID of the logged-in user.
        """
        self.user_id = user_id
        self.show_home_page()

    def show_home_page(self):
        """Displays the home page."""
        self.show_frame(
            0,
            0,
            HomePage,
            self.user_id,
            self.server_url,
            lambda review_type: self.show_flashcard_reviewer(self.user_id, review_type),
            lambda: self.on_create_set_click(self.user_id),
            lambda: self.on_library_click(self.user_id),
            lambda: self.show_login_page(),
        )

    def on_create_set_click(self, user_id):
        """Displays the create set page."""
        self.show_frame(1, 2, CreateSetPage, user_id, self.show_home_page)

    def show_flashcard_reviewer(self, user_id, review_type, set_name=None):
        """Displays the flashcard reviewer page."""
        if review_type == "scheduled":
            self.show_frame(
                1, 2, ScheduledFlashcardReviewer, user_id, self.show_home_page
            )
        elif review_type == "unscheduled":
            self.show_frame(
                1,
                2,
                UnscheduledFlashcardReviewer,
                user_id,
                lambda: self.on_library_click(user_id),
                set_name,
            )

    def on_library_click(self, user_id):
        """Displays the library page."""
        self.show_frame(
            0,
            0,
            LibraryPage,
            user_id,
            lambda review_type, set_name=None: self.show_flashcard_reviewer(
                self.user_id, review_type, set_name
            ),
            self.show_home_page,
        )


def main():
    root = ctk.CTk()
    app = PhysicsApp(master=root)
    app.grid(row=0, column=0, sticky="nsew")
    root.title("Physics App")

    # Configure root grid
    root.grid_rowconfigure(0, weight=1)
    root.grid_columnconfigure(0, weight=1)

    # Set window size to fullscreen
    width, height = root.winfo_screenwidth(), root.winfo_screenheight()
    root.geometry(f"{width}x{height}")

    # Start the main event loop
    root.mainloop()


if __name__ == "__main__":
    main()
