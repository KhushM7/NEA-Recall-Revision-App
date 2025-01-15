import customtkinter as ctk
from tkinter import messagebox

from physics_app.utilities.server_utilities.flashcard_handler import FlashcardHandler
from physics_app.views.import_set_page import ImportSetPage


class CreateSetPage(ctk.CTkFrame):
    def __init__(self, parent, user_id, on_close):
        super().__init__(parent)
        self.root = parent
        self.root.configure(fg_color="#f2f6fa")
        self.user_id = user_id
        self.on_close = on_close
        self.flashcard_handler = FlashcardHandler(server_url="http://127.0.0.1:5000")

        # Set background color and layout configurations
        self.configure(fg_color="#f2f6fa")  # Light blue background

        # Configure grid layout for centering
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        self.grid_rowconfigure(2, weight=1)

        # Create an internal frame to center the content
        self.content_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.content_frame.grid(row=1, column=1, sticky="nsew")
        self.content_frame.grid_columnconfigure(0, weight=1)
        self.content_frame.grid_columnconfigure(1, weight=1)
        self.content_frame.grid_columnconfigure(2, weight=1)
        self.content_frame.grid_rowconfigure(0, weight=1)
        self.content_frame.grid_rowconfigure(1, weight=1)
        self.content_frame.grid_rowconfigure(2, weight=1)

        self.create_widgets()

    def create_widgets(self):
        # Main Frame to hold all widgets
        main_frame = ctk.CTkFrame(self.content_frame, fg_color="transparent")
        main_frame.grid(row=1, column=1, sticky="nsew", padx=20, pady=20)
        main_frame.grid_columnconfigure(0, weight=1)
        main_frame.grid_columnconfigure(1, weight=0)
        main_frame.grid_columnconfigure(2, weight=1)
        main_frame.grid_rowconfigure(0, weight=1)
        main_frame.grid_rowconfigure(1, weight=1)
        main_frame.grid_rowconfigure(2, weight=1)
        # Title Label
        self.title_label = ctk.CTkLabel(
            main_frame,
            text="Create Flashcard Set",
            font=("Arial", 20, "bold"),
            text_color="#1e90ff",
        )
        self.title_label.grid(row=0, column=1, pady=(20, 10))

        # Input Frame for Set Name, Front, and Back
        input_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        input_frame.grid(row=1, column=1, pady=20, padx=20, sticky="ew")
        input_frame.grid_columnconfigure(0, weight=1)

        # Set Name Entry
        self.set_name_label = ctk.CTkLabel(
            input_frame,
            text="Set Name:",
            anchor="w",
            font=("Arial", 14),
            text_color="#333333",
        )
        self.set_name_label.grid(row=0, column=0, sticky="w", pady=5)
        self.set_name_entry = ctk.CTkEntry(
            input_frame, placeholder_text="Enter set name...", corner_radius=10
        )
        self.set_name_entry.grid(row=1, column=0, sticky="ew", pady=5)

        # Front of Card Textbox
        self.front_label = ctk.CTkLabel(
            input_frame,
            text="Front of Card:",
            anchor="w",
            font=("Arial", 14),
            text_color="#333333",
        )
        self.front_label.grid(row=2, column=0, sticky="w", pady=5)
        self.front_textbox = ctk.CTkTextbox(
            input_frame, wrap="word", height=100, corner_radius=10
        )
        self.front_textbox.grid(row=3, column=0, sticky="ew", pady=5)

        # Back of Card Textbox
        self.back_label = ctk.CTkLabel(
            input_frame,
            text="Back of Card:",
            anchor="w",
            font=("Arial", 14),
            text_color="#333333",
        )
        self.back_label.grid(row=4, column=0, sticky="w", pady=5)
        self.back_textbox = ctk.CTkTextbox(
            input_frame, wrap="word", height=100, corner_radius=10
        )
        self.back_textbox.grid(row=5, column=0, sticky="ew", pady=5)

        # Buttons Frame
        button_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        button_frame.grid(row=2, column=1, pady=(10, 20))

        # Import Set Button
        self.import_button = ctk.CTkButton(
            button_frame,
            text="Import Set",
            command=self.import_set,
            fg_color="#5dd8d5",
            hover_color="#4cc0b8",
            text_color="white",
            corner_radius=15,
        )
        self.import_button.grid(row=0, column=0, padx=10)

        # Save Flashcard Button
        self.save_button = ctk.CTkButton(
            button_frame,
            text="Save Flashcard",
            command=self.save_flashcard,
            fg_color="#1e90ff",
            hover_color="#1a7dc0",
            text_color="white",
            corner_radius=15,
        )
        self.save_button.grid(row=0, column=1, padx=10)

        # Close Button
        self.close_button = ctk.CTkButton(
            button_frame,
            text="Close",
            command=self.on_close,
            fg_color="#ff4f4f",
            hover_color="#e43e3e",
            text_color="white",
            corner_radius=15,
        )
        self.close_button.grid(row=0, column=2, padx=10)

    def save_flashcard(self):
        # Collect input and validate
        set_name = self.set_name_entry.get().strip()
        front_text = self.front_textbox.get("1.0", "end-1c").strip()
        back_text = self.back_textbox.get("1.0", "end-1c").strip()

        if not set_name or not front_text or not back_text:
            messagebox.showerror("Error", "All fields must be filled out.")
            return

        flashcard_data = {"set_name": set_name, "front": front_text, "back": back_text}
        self.flashcard_handler.create_flashcard(self.user_id, flashcard_data)

        # Clear inputs
        self.front_textbox.delete("1.0", "end")
        self.back_textbox.delete("1.0", "end")

    def import_set(self):
        # Placeholder function for Import Set feature
        ImportSetPage(self.root, self.user_id)
