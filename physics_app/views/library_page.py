import customtkinter as ctk
from customtkinter import CTkScrollableFrame
from physics_app.utilities.server_utilities.flashcard_handler import FlashcardHandler
from physics_app.utilities.setup_icons import (
    setup_edit_icon,
    setup_close_icon,
    setup_bin_icon,
)
from physics_app.utilities.tooltip import Tooltip
from physics_app.views.edit_set_page import EditSetWindow


class LibraryPage(ctk.CTkFrame):
    def __init__(self, parent, user_id: int, on_review_click=None, on_close=None):
        super().__init__(parent)
        self.configure(fg_color="white")
        self.master = parent
        self.flashcard_handler = FlashcardHandler(server_url="http://127.0.0.1:5000")
        self.edit_icon, _ = setup_edit_icon()
        self.close_icon, _ = setup_close_icon()
        self.bin_icon, _ = setup_bin_icon()
        self.user_id = user_id
        self.on_close = on_close
        self.on_review_click = on_review_click
        self.set_names_with_num_terms = (
            self.flashcard_handler.get_set_names_with_num_terms(self.user_id)
        )
        self.setup_master_grid()
        self.create_widgets()

    def setup_master_grid(self):
        self.master.configure(fg_color="white")
        self.master.grid_rowconfigure(0, weight=0)
        self.master.grid_rowconfigure(1, weight=2)
        self.master.grid_rowconfigure(2, weight=1)
        self.master.grid_columnconfigure(0, weight=1)
        self.master.grid_columnconfigure(1, weight=1)
        self.master.grid_columnconfigure(2, weight=1)

    def create_widgets(self):
        central_frame = ctk.CTkFrame(
            self.master, height=self.master.winfo_height(), fg_color="#f0f0f0"
        )
        central_frame.grid(row=1, column=1, columnspan=3, sticky="nsew")

        # Configure central_frame to expand properly
        central_frame.grid_rowconfigure(0, weight=0)
        central_frame.grid_rowconfigure(1, weight=1)  # Expand scrollable frame
        central_frame.grid_columnconfigure(0, weight=0)
        central_frame.grid_columnconfigure(1, weight=1)
        central_frame.grid_columnconfigure(0, weight=0)

        # Search bar (shorter width to accommodate close button)
        self.search_var = ctk.StringVar()
        self.search_entry = ctk.CTkEntry(
            central_frame,
            textvariable=self.search_var,
            height=40,  # Thicker
            width=400,  # Adjusted width
            font=ctk.CTkFont(size=16),  # Larger font
        )
        self.search_entry.grid(row=0, column=0, padx=(20, 5), pady=20, sticky="ew")
        self.add_placeholder(self.search_entry, "Search")
        self.search_entry.bind("<KeyRelease>", self.search_sets)

        # Close button
        self.close_button = ctk.CTkButton(
            central_frame,
            text="",
            image=self.close_icon,
            hover_color="#f81424",
            command=self.on_close,
            width=30,
        )
        self.close_button.grid(row=0, column=1, padx=(5, 20), pady=20, sticky="e")

        # Scrollable container for sets
        self.sets_container = CTkScrollableFrame(central_frame, fg_color="transparent")
        self.sets_container.grid(
            row=1, column=0, columnspan=3, padx=20, pady=10, sticky="nsew"
        )
        self.sets_container.grid_columnconfigure(0, weight=0)
        self.sets_container.grid_columnconfigure(1, weight=1)
        self.sets_container.grid_columnconfigure(2, weight=0)
        self.display_sets()

    def add_placeholder(self, entry, placeholder):
        entry.insert(0, placeholder)
        entry.configure(text_color="grey")
        entry.bind(
            "<FocusIn>", lambda event: self.clear_placeholder(entry, placeholder)
        )
        entry.bind(
            "<FocusOut>", lambda event: self.restore_placeholder(entry, placeholder)
        )

    def clear_placeholder(self, entry, placeholder):
        if entry.get() == placeholder:
            entry.delete(0, "end")

    def restore_placeholder(self, entry, placeholder):
        if entry.get() == "":
            entry.insert(0, placeholder)

    def display_sets(self):
        # Clear existing widgets
        for widget in self.sets_container.winfo_children():
            widget.destroy()

        # Display each set
        for idx, (set_name, num_terms) in enumerate(
            self.set_names_with_num_terms.items()
        ):
            self.create_set_widget(set_name, num_terms, idx)

    def create_set_widget(self, set_name: str, num_terms: int, row: int):
        def on_set_click(event):
            widget = event.widget
            if widget != edit_button:  # Ensure edit button is excluded
                if self.on_review_click:
                    self.on_review_click("unscheduled", set_name=set_name)

        set_frame = ctk.CTkFrame(
            self.sets_container, corner_radius=10, fg_color="white", cursor="hand2"
        )
        set_frame.grid(row=row, column=1, padx=20, pady=10, sticky="ew")

        set_frame.grid_columnconfigure(0, weight=1)
        set_frame.grid_columnconfigure(1, weight=0)

        # Bind click event to the set_frame
        set_frame.bind("<Button-1>", on_set_click)

        # Set name (large font)
        set_label = ctk.CTkLabel(set_frame, text=set_name, font=ctk.CTkFont(size=18))
        set_label.grid(row=0, column=0, padx=10, pady=10, sticky="w")

        # Number of terms (small grey text)
        terms_label = ctk.CTkLabel(
            set_frame,
            text=f"{num_terms} terms",
            font=ctk.CTkFont(size=12),
            text_color="grey",
        )
        terms_label.grid(row=0, column=1, padx=10, pady=5, sticky="ne")

        # Edit button
        edit_button = ctk.CTkButton(
            set_frame,
            image=self.edit_icon,
            text="",
            fg_color="transparent",
            hover_color="#BDE7BD",
            width=30,
            height=30,
            command=lambda: EditSetWindow(
                self,
                set_name,
                self.flashcard_handler.get_flashcards_by_set(self.user_id, set_name),
                self.save_set_callback,
            ),
        )
        edit_button.grid(row=1, column=1, padx=10, pady=10, sticky="ne")
        Tooltip(
            edit_button, background_color="transparent", hover_delay=150, text="Edit"
        )

        # Prevent edit_button clicks from propagating to set_frame
        edit_button.bind("<Button-1>", lambda e: "break")

        # Delete button
        delete_button = ctk.CTkButton(
            set_frame,
            image=self.bin_icon,
            text="",
            fg_color="transparent",
            hover_color="#FFB6B3",
            width=30,
            height=30,
            command=lambda: self.delete_set_and_refresh(set_name, set_frame),
        )
        # Place delete button at bottom left
        delete_button.grid(row=1, column=0, padx=10, pady=10, sticky="sw")
        Tooltip(
            delete_button,
            background_color="transparent",
            hover_delay=150,
            text="Delete",
        )

        # Prevent delete_button clicks from propagating to set_frame
        delete_button.bind("<Button-1>", lambda e: "break")

    def search_sets(self, event=None):
        search_text = self.search_var.get().lower()
        matches = [
            name
            for name in self.set_names_with_num_terms
            if search_text in name.lower()
        ]
        self.display_filtered_sets(matches)

    def display_filtered_sets(self, matches):
        for widget in self.sets_container.winfo_children():
            widget.destroy()

        for idx, set_name in enumerate(matches):
            self.create_set_widget(
                set_name, self.set_names_with_num_terms[set_name], idx
            )

    def save_set_callback(self, set_name, updated_flashcards, deleted_card_ids):
        # Update existing cards
        for card in updated_flashcards:
            if card["card_id"]:
                self.flashcard_handler.update_flashcard(self.user_id, card)
            else:
                card_data = {
                    "set_name": set_name,
                    "front": card["front"],
                    "back": card["back"],
                }
                self.flashcard_handler.create_flashcard(self.user_id, card_data)
                pass

        # Delete marked cards
        if deleted_card_ids:
            for card_id in deleted_card_ids:
                self.flashcard_handler.delete_card(self.user_id, card_id)
                pass

    def delete_set_and_refresh(self, set_name, set_frame):
        self.flashcard_handler.delete_set(self.user_id, set_name)
        set_frame.destroy()
