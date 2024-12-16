import customtkinter as ctk
from typing import List, Dict, Any
from physics_app.utilities.server_utilities.flashcard_handler import FlashcardHandler
from physics_app.views.choose_set_to_review import ChooseSetToReview


class FlashcardReviewer(ctk.CTkFrame):
    def __init__(self, root, user_id, on_close, review_type):
        super().__init__(root)
        self.root = root
        self.user_id = user_id
        self.on_close = on_close
        self.review_type = review_type
        self.flashcard_handler = FlashcardHandler(server_url="http://127.0.0.1:5000")
        self.flashcards: List[Dict[str, Any]] = []
        self.current_index = 0
        self.is_flipped = False
        self.correct_count = 0
        self.wrong_count = 0

        # Configure layout and initialize components
        self.configure(fg_color="#f4f4f4")

        self.create_widgets()
        self.load_flashcards()

    def create_widgets(self):
        # Configure grid weights to center the content
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        self.grid_rowconfigure(2, weight=1)
        self.grid_rowconfigure(3, weight=1)
        self.grid_rowconfigure(4, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=0)
        self.grid_columnconfigure(2, weight=0)
        self.grid_columnconfigure(3, weight=0)
        self.grid_columnconfigure(4, weight=0)
        self.grid_columnconfigure(5, weight=0)
        self.grid_columnconfigure(6, weight=1)

        # Close button to return to the home page
        self.close_button = ctk.CTkButton(
            self, text="X", command=self.on_close, width=30
        )
        self.close_button.grid(row=0, column=6, sticky="ne", padx=10, pady=10)

        self.flashcard_label = ctk.CTkLabel(
            self,
            text="Loading...",
            font=("Arial", 24),
            width=500,
            height=250,
            fg_color="#ffffff",
            wraplength=480,
            corner_radius=10,
        )
        self.flashcard_label.grid(row=1, column=1, columnspan=5, pady=20, sticky="nsew")
        self.flashcard_label.bind("<Button-1>", lambda event: self.flip_card())

        self.instruction_label = ctk.CTkLabel(
            self,
            text="",
            font=("Arial", 12),
            fg_color="#f4f4f4",
            text_color="grey",
        )
        self.instruction_label.grid(
            row=2, column=1, columnspan=5, pady=(5, 20), sticky="nsew"
        )

        # Create buttons with equal spacing and centered
        self.again_button = ctk.CTkButton(self, text="Again", command=self.mark_again)
        self.again_button.grid(row=3, column=2, padx=10, sticky="ew")
        self.hard_button = ctk.CTkButton(self, text="Hard", command=self.mark_hard)
        self.hard_button.grid(row=3, column=3, padx=10, sticky="ew")
        self.good_button = ctk.CTkButton(self, text="Good", command=self.mark_good)
        self.good_button.grid(row=3, column=4, padx=10, sticky="ew")
        self.easy_button = ctk.CTkButton(self, text="Easy", command=self.mark_easy)
        self.easy_button.grid(row=3, column=5, padx=10, sticky="ew")

        # Create buttons for unscheduled review
        self.correct_button = ctk.CTkButton(
            self, text="Correct", command=self.mark_correct
        )
        self.wrong_button = ctk.CTkButton(self, text="Wrong", command=self.mark_wrong)

    def load_flashcards(self):
        """Fetch flashcards from the server and display the first one."""
        if self.review_type == "scheduled":
            self.flashcards = self.flashcard_handler.get_due_flashcards(self.user_id)
            if self.flashcards:
                self.current_index = 0
                self.display_flashcard()
            else:
                self.flashcard_label.configure(text="No flashcards available.")
                self.disable_buttons()
        elif self.review_type == "unscheduled":
            sets = self.flashcard_handler.get_sets(self.user_id)
            chooser = ChooseSetToReview(self, sets)
            chosen_set = chooser.get_chosen_set()
            self.flashcards = self.flashcard_handler.get_flashcards_by_set(
                self.user_id, chosen_set
            )
            self.current_index = 0
            self.display_flashcard()
            self.show_unscheduled_buttons()

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
            if self.review_type == "unscheduled":
                self.show_results()

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

    def mark_correct(self):
        """Handle 'Correct' button press."""
        self.correct_count += 1
        self.next_flashcard()

    def mark_wrong(self):
        """Handle 'Wrong' button press."""
        self.wrong_count += 1
        self.next_flashcard()

    def show_unscheduled_buttons(self):
        """Show 'Correct' and 'Wrong' buttons for unscheduled review."""
        self.again_button.grid_remove()
        self.hard_button.grid_remove()
        self.good_button.grid_remove()
        self.easy_button.grid_remove()
        self.correct_button.grid(row=3, column=3, padx=10, sticky="ew")
        self.wrong_button.grid(row=3, column=4, padx=10, sticky="ew")

    def show_results(self):
        """Display the results of the review."""
        result_text = f"Correct: {self.correct_count}\nWrong: {self.wrong_count}"
        self.flashcard_label.configure(text=result_text)
        self.instruction_label.configure(text="Review complete.")

    def disable_buttons(self):
        """Disable interaction buttons."""
        self.again_button.configure(state="disabled")
        self.hard_button.configure(state="disabled")
        self.good_button.configure(state="disabled")
        self.easy_button.configure(state="disabled")
        self.correct_button.configure(state="disabled")
        self.wrong_button.configure(state="disabled")
