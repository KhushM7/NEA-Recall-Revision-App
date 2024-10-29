import customtkinter as ctk

from physics_app.views.flashcard_reviewer import FlashcardReviewer


class HomePage(ctk.CTkFrame):
    def __init__(self, master, server_url, user_id):
        super().__init__(master)
        self.server_url = server_url
        self.user_id = user_id
        self.label = ctk.CTkLabel(self, text="Home", font=("Arial", 24))
        self.label.grid(row=0, column=0, pady=20)

        self.review_button = ctk.CTkButton(
            self,
            text="Review",
            command=lambda: master.switch_frame(FlashcardReviewer(self), user_id),
        )
        self.review_button.grid(row=1, column=0, pady=20)
