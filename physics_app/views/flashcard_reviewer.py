import customtkinter as ctk
from typing import List, Dict, Any
from physics_app.utilities.server_utilities.flashcard_handler import FlashcardHandler
from physics_app.utilities.setup_icons import setup_close_icon


class BaseFlashcardReviewer(ctk.CTkFrame):
    def __init__(self, parent, user_id, on_close):
        super().__init__(parent)
        self.root = parent
        self.root.configure(fg_color="#f4f4f4")
        self.user_id = user_id
        self.on_close = on_close
        self.flashcard_handler = FlashcardHandler(server_url="http://127.0.0.1:5000")
        self.flashcards: List[Dict[str, Any]] = []
        self.current_index = 0
        self.is_flipped = False
        self.correct_count = 0
        self.wrong_count = 0
        self.close_icon, self.close_icon_size = setup_close_icon()

        # Configure layout and background
        self.configure(fg_color="#f4f4f4")
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        self.grid_rowconfigure(2, weight=1)

        # Centered content frame
        self.content_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.content_frame.grid(row=1, column=1, sticky="nsew")
        self.content_frame.grid_columnconfigure(0, weight=1)
        self.content_frame.grid_rowconfigure(0, weight=1)
        self.content_frame.grid_rowconfigure(1, weight=1)
        self.content_frame.grid_rowconfigure(2, weight=1)

        self.create_widgets()

    def create_widgets(self):
        # Main Frame to hold all widgets
        main_frame = ctk.CTkFrame(self.content_frame, fg_color="transparent")
        main_frame.grid(row=1, column=0, padx=20, pady=20, sticky="nsew")
        main_frame.grid_columnconfigure(0, weight=1)
        main_frame.grid_columnconfigure(1, weight=1)
        main_frame.grid_columnconfigure(2, weight=1)

        # Close Button
        self.close_button = ctk.CTkButton(
            main_frame,
            text="",
            image=self.close_icon,
            hover_color="#f81424",
            command=self.on_close,
            width=30,
        )
        self.close_button.grid(row=0, column=2, sticky="ne", padx=10, pady=10)

        # Flashcard Label
        self.flashcard_label = ctk.CTkLabel(
            main_frame,
            text="Loading...",
            font=("Arial", 24),
            width=500,
            height=250,
            fg_color="#ffffff",
            wraplength=480,
            corner_radius=10,
        )
        self.flashcard_label.grid(row=1, column=1, pady=20, sticky="nsew")
        self.flashcard_label.bind("<Button-1>", lambda event: self.flip_card())

        self.instruction_label = ctk.CTkLabel(
            main_frame,
            text="Click the card to flip it.",
            font=("Arial", 12),
            fg_color="transparent",
            text_color="grey",
        )
        self.instruction_label.grid(row=2, column=1, pady=(5, 20), sticky="nsew")

        # Button Frame
        self.button_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        self.button_frame.grid(row=3, column=1, pady=20, sticky="ew")
        self.button_frame.grid_columnconfigure(0, weight=1)
        self.button_frame.grid_columnconfigure(1, weight=1)
        self.button_frame.grid_columnconfigure(2, weight=1)
        self.button_frame.grid_columnconfigure(3, weight=1)

        # Score Frame
        self.score_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        self.score_frame.grid_rowconfigure(0, weight=1)
        self.score_frame.grid_columnconfigure(0, weight=1)
        self.score_frame.grid_columnconfigure(1, weight=1)

    def flip_card(self):
        if self.current_index < len(self.flashcards):
            self.is_flipped = not self.is_flipped
            current_card = self.flashcards[self.current_index]
            target_text = (
                current_card["back"] if self.is_flipped else current_card["front"]
            )
            self.flashcard_label.configure(text=target_text)

    def next_flashcard(self):
        self.current_index += 1
        self.display_flashcard()

    def display_flashcard(self):
        if self.current_index < len(self.flashcards):
            self.is_flipped = False
            current_card = self.flashcards[self.current_index]
            self.flashcard_label.configure(text=current_card["front"])
            self.instruction_label.configure(text="Click the card to flip it")
        else:
            self.flashcard_label.configure(text="Review complete.")
            self.disable_buttons()
            self.show_results()

    def disable_buttons(self):
        """Disable interaction buttons."""
        buttons = [
            getattr(self, "again_button", None),
            getattr(self, "hard_button", None),
            getattr(self, "good_button", None),
            getattr(self, "easy_button", None),
            getattr(self, "correct_button", None),
            getattr(self, "wrong_button", None),
        ]
        for button in buttons:
            if button is not None:
                button.configure(state="disabled")

    def process_rating(self, rating: str):
        current_card = self.flashcards[self.current_index]
        self.flashcard_handler.submit_rating(
            self.user_id, current_card["card_id"], rating
        )

    def show_results(self):
        # Default behavior: Do nothing
        pass


class ScheduledFlashcardReviewer(BaseFlashcardReviewer):
    def __init__(self, parent, user_id, on_close):
        super().__init__(parent, user_id, on_close)
        self.create_rating_buttons()
        self.load_flashcards()

    def create_rating_buttons(self):
        self.again_button = ctk.CTkButton(
            self.button_frame, text="Again", command=self.mark_again
        )
        self.again_button.grid(row=0, column=0, padx=5, sticky="ew")

        self.hard_button = ctk.CTkButton(
            self.button_frame, text="Hard", command=self.mark_hard
        )
        self.hard_button.grid(row=0, column=1, padx=5, sticky="ew")

        self.good_button = ctk.CTkButton(
            self.button_frame, text="Good", command=self.mark_good
        )
        self.good_button.grid(row=0, column=2, padx=5, sticky="ew")

        self.easy_button = ctk.CTkButton(
            self.button_frame, text="Easy", command=self.mark_easy
        )
        self.easy_button.grid(row=0, column=3, padx=5, sticky="ew")

    def mark_again(self):
        self.process_rating("Again")
        self.next_flashcard()

    def mark_hard(self):
        self.process_rating("Hard")
        self.next_flashcard()

    def mark_good(self):
        self.process_rating("Good")
        self.next_flashcard()

    def mark_easy(self):
        self.process_rating("Easy")
        self.next_flashcard()

    def load_flashcards(self):
        self.flashcards = self.flashcard_handler.get_due_flashcards(self.user_id)
        if self.flashcards:
            self.display_flashcard()
        else:
            self.flashcard_label.configure(text="No flashcards available.")
            self.disable_buttons()


class UnscheduledFlashcardReviewer(BaseFlashcardReviewer):
    def __init__(self, parent, user_id, on_close, set_name=None):
        super().__init__(parent, user_id, on_close)
        self.score_frame.grid(row=3, column=1, padx=5, sticky="ew")

        self.correct_button = ctk.CTkButton(
            self.score_frame, text="Correct", command=self.mark_correct
        )
        self.correct_button.grid(row=0, column=0, padx=5, sticky="ew")

        self.wrong_button = ctk.CTkButton(
            self.score_frame, text="Wrong", command=self.mark_wrong
        )
        self.wrong_button.grid(row=0, column=1, padx=5, sticky="ew")

        self.load_flashcards(set_name)

    def load_flashcards(self, set_name=None):
        self.flashcards = self.flashcard_handler.get_flashcards_by_set(
            self.user_id, set_name
        )
        if self.flashcards:
            self.display_flashcard()
        else:
            self.flashcard_label.configure(text="No flashcards available.")
            self.disable_buttons()

    def mark_correct(self):
        self.correct_count += 1
        self.next_flashcard()

    def mark_wrong(self):
        self.wrong_count += 1
        self.next_flashcard()

    def show_results(self):
        result_text = f"Correct: {self.correct_count}\nWrong: {self.wrong_count}"
        self.flashcard_label.configure(text=result_text)
        self.instruction_label.configure(text="Review complete.")
