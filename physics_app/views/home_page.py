import tkinter as tk
import customtkinter as ctk

from physics_app.views.flashcard_library import FlashcardLibraryScreen


class HomePage(tk.Frame):
    def __init__(self, master, server_url: str):
        super().__init__(master)
        self.master = master
        self.server_url = server_url

        self.master.grid_rowconfigure(0, weight=0)
        self.master.grid_rowconfigure(1, weight=0)
        self.master.grid_rowconfigure(2, weight=0)
        self.master.grid_columnconfigure(0, weight=0)
        self.create_widgets()

    def create_widgets(self):
        self.flashcard_library_button = ctk.CTkButton(
            self.master,
            text="Flashcard Library",
            command=lambda: FlashcardLibraryScreen(self.master, self.server_url),
        )
        self.flashcard_library_button.grid(row=0, column=0, sticky="nsew")
