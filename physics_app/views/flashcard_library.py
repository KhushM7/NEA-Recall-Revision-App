import tkinter as tk


class FlashcardLibraryScreen(tk.Frame):
    def __init__(self, master, server_url: str):
        super().__init__(master)
        self.master = master
        self.server_url = server_url
        self.createwidgets()

    def createwidgets(self):
        self.flashcard_library_label = tk.Label(
            self.master,
            text="Flashcard Library",
            font=("Arial", 24),
        )
        self.flashcard_library_label.grid(row=0, column=0, sticky="nsew")

        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)
