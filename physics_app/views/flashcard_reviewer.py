import customtkinter as ctk


class FlashcardReviewer(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        # self.user_id = user_id
        self.card_display = ctk.CTkLabel(
            self,
            text=f"{self.user_id}: Front of the Flashcard",
            font=("Arial", 18),
            width=400,
            height=200,
        )
        self.card_display.grid(row=0, column=0, pady=40, columnspan=5)

        self.button_frame = ctk.CTkFrame(self)
        self.button_frame.grid(row=1, column=0, pady=20, columnspan=5)

        self.flip_button = ctk.CTkButton(self.button_frame, text="Flip")
        self.flip_button.grid(row=0, column=0, padx=10)

        self.again_button = ctk.CTkButton(self.button_frame, text="Again")
        self.again_button.grid(row=0, column=1, padx=10)

        self.hard_button = ctk.CTkButton(self.button_frame, text="Hard")
        self.hard_button.grid(row=0, column=2, padx=10)

        self.good_button = ctk.CTkButton(self.button_frame, text="Good")
        self.good_button.grid(row=0, column=3, padx=10)

        self.easy_button = ctk.CTkButton(self.button_frame, text="Easy")
        self.easy_button.grid(row=0, column=4, padx=10)
