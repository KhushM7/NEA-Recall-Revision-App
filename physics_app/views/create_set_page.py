import customtkinter as ctk
from tkinter import messagebox

from physics_app.utilities.server_utilities.flashcard_handler import FlashcardHandler


class CreateSetPage(ctk.CTkFrame):
    def __init__(self, root, user_id, on_close):
        super().__init__(root)
        self.root = root
        self.user_id = user_id
        self.on_close = on_close
        self.flashcard_handler = FlashcardHandler(server_url="http://127.0.0.1:5000")
        self.create_widgets()

    def create_widgets(self):
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        self.grid_rowconfigure(2, weight=1)
        self.grid_rowconfigure(3, weight=1)
        self.grid_rowconfigure(4, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=1)
        self.grid_columnconfigure(3, weight=1)

        self.set_name_label = ctk.CTkLabel(self, text="Set Name:")
        self.set_name_label.grid(row=0, column=1, pady=10, sticky="e")
        self.set_name_entry = ctk.CTkEntry(self)
        self.set_name_entry.grid(row=0, column=2, pady=10, sticky="w")

        self.front_label = ctk.CTkLabel(self, text="Front of card:")
        self.front_label.grid(row=1, column=1, pady=10, sticky="e")
        self.front_entry = ctk.CTkEntry(self)
        self.front_entry.grid(row=1, column=2, pady=10, sticky="w")

        self.back_label = ctk.CTkLabel(self, text="Back of card:")
        self.back_label.grid(row=2, column=1, pady=10, sticky="e")
        self.back_entry = ctk.CTkEntry(self)
        self.back_entry.grid(row=2, column=2, pady=10, sticky="w")

        self.save_button = ctk.CTkButton(
            self, text="Save Flashcard", command=self.save_flashcard
        )
        self.save_button.grid(row=3, column=1, columnspan=2, pady=20)

        self.close_button = ctk.CTkButton(self, text="Close", command=self.on_close)
        self.close_button.grid(row=4, column=1, columnspan=2, pady=10)

    def save_flashcard(self):
        set_name = self.set_name_entry.get().strip()
        front_text = self.front_entry.get().strip()
        back_text = self.back_entry.get().strip()

        if not set_name or not front_text or not back_text:
            messagebox.showerror("Error", "All fields must be filled out.")
            return

        flashcard_data = {"set_name": set_name, "front": front_text, "back": back_text}
        self.flashcard_handler.create_flashcard(self.user_id, flashcard_data)

        self.front_entry.delete(0, "end")
        self.back_entry.delete(0, "end")


# Example usage
if __name__ == "__main__":
    root = ctk.CTk()
    app = CreateSetPage(root, user_id=1, on_close=root.destroy)
    app.grid(row=0, column=0, sticky="nsew")
    root.mainloop()
