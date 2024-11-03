import customtkinter as ctk
from datetime import datetime
from typing import List, Dict, Any
from physics_app.utilities.server_utilities.flashcard_handler import FlashcardHandler


class FlashcardReviewer(ctk.CTkFrame):
    def __init__(self, root, user_id, on_close):
        super().__init__(root)
        self.user_id = user_id
        self.on_close = on_close
        self.flashcard_handler = FlashcardHandler(server_url="http://127.0.0.1:5000")
        self.flashcards: List[Dict[str, Any]] = []
        self.current_index = 0
        self.is_flipped = False

        # Configure layout and initialize components
        self.configure(fg_color="#f4f4f4")
        self.create_widgets()
        self.load_flashcards()

    def create_widgets(self):
        # Close button to return to the home page
        self.close_button = ctk.CTkButton(
            self, text="X", command=self.on_close, width=30
        )
        self.close_button.grid(row=0, column=4, sticky="ne", padx=10, pady=10)

        # Flashcard display area
        self.flashcard_label = ctk.CTkLabel(
            self,
            text="Loading...",
            font=("Arial", 24),
            width=500,
            height=250,
            fg_color="#ffffff",
            corner_radius=10,
        )
        self.flashcard_label.grid(row=1, column=0, columnspan=5, pady=20)
        self.flashcard_label.bind(
            "<Button-1>", lambda event: self.flip_card()
        )  # Flip on click

        # Instruction label below the flashcard
        self.instruction_label = ctk.CTkLabel(
            self,
            text="",
            font=("Arial", 12),
            fg_color="#f4f4f4",
            text_color="grey",
        )
        self.instruction_label.grid(row=2, column=0, columnspan=5, pady=(5, 20))

        # Buttons for rating flashcards
        self.again_button = ctk.CTkButton(self, text="Again", command=self.mark_again)
        self.again_button.grid(row=3, column=0, padx=10)
        self.hard_button = ctk.CTkButton(self, text="Hard", command=self.mark_hard)
        self.hard_button.grid(row=3, column=1, padx=10)
        self.good_button = ctk.CTkButton(self, text="Good", command=self.mark_good)
        self.good_button.grid(row=3, column=2, padx=10)
        self.easy_button = ctk.CTkButton(self, text="Easy", command=self.mark_easy)
        self.easy_button.grid(row=3, column=3, padx=10)

    def load_flashcards(self):
        """Fetch flashcards from the server and display the first one."""
        self.flashcards = self.flashcard_handler.get_due_flashcards(self.user_id)
        if self.flashcards:
            self.current_index = 0
            self.display_flashcard()
        else:
            self.flashcard_label.configure(text="No flashcards available.")
            self.disable_buttons()

    def display_flashcard(self):
        """Display the current flashcard."""
        if self.current_index < len(self.flashcards):
            self.is_flipped = False
            current_card = self.flashcards[self.current_index]
            self.flashcard_label.configure(text=current_card["front"])
            self.instruction_label.configure(text="Click the card to flip it")
        else:
            self.flashcard_label.configure(text="Review complete.")
            self.disable_buttons()

    def flip_card(self):
        """Flip between the front and back of the current flashcard."""
        if self.current_index < len(self.flashcards):
            self.is_flipped = not self.is_flipped
            current_card = self.flashcards[self.current_index]
            target_text = (
                current_card["back"] if self.is_flipped else current_card["front"]
            )
            self.animate_flip(target_text)

    def animate_flip(self, target_text):
        """Creates a basic flipping animation."""
        self.flashcard_label.configure(text="")
        self.after(100, lambda: self.flashcard_label.configure(text=target_text))

    def next_flashcard(self):
        """Move to the next flashcard."""
        self.current_index += 1
        self.display_flashcard()

    def mark_again(self):
        """Handle 'Again' rating."""
        self.process_rating("Again")
        self.next_flashcard()

    def mark_hard(self):
        """Handle 'Hard' rating."""
        self.process_rating("Hard")
        self.next_flashcard()

    def mark_good(self):
        """Handle 'Good' rating."""
        self.process_rating("Good")
        self.next_flashcard()

    def mark_easy(self):
        """Handle 'Easy' rating."""
        self.process_rating("Easy")
        self.next_flashcard()

    def process_rating(self, rating: str):
        """Process the rating and update the card state."""
        current_card = self.flashcards[self.current_index]
        response = self.flashcard_handler.submit_rating(
            self.user_id, current_card["card_id"], rating
        )
        if response.get("success"):
            print(f"Rating '{rating}' for card ID {current_card['card_id']} submitted.")
        else:
            print("Failed to submit rating.")

    def disable_buttons(self):
        """Disable interaction buttons."""
        self.again_button.configure(state="disabled")
        self.hard_button.configure(state="disabled")
        self.good_button.configure(state="disabled")
        self.easy_button.configure(state="disabled")
