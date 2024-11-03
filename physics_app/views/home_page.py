import customtkinter as ctk


class HomePage(ctk.CTkFrame):
    def __init__(self, root, on_review_click):
        super().__init__(root)
        review_button = ctk.CTkButton(root, text="Review", command=on_review_click)
        review_button.grid(row=0, column=0, pady=20)
