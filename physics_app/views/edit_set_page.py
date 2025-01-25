import customtkinter as ctk
from physics_app.utilities.setup_icons import setup_plus_icon, setup_bin_icon


class EditSetWindow(ctk.CTkToplevel):
    def __init__(self, master, set_name, flashcards, save_callback):
        super().__init__(master)

        self.set_name = set_name
        self.flashcards = flashcards
        self.save_callback = save_callback
        self.deleted_card_ids = []

        self.icon_plus, _ = setup_plus_icon()
        self.icon_bin, _ = setup_bin_icon()

        self.title("Edit Set")
        self.geometry("800x600")
        self.grab_set()
        self.transient(master)

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        ctk.CTkLabel(self, text=f"Set Name: {self.set_name}").grid(
            row=0, column=0, sticky="w", padx=(20, 0), pady=(10, 5)
        )
        self.grid_columnconfigure(1, weight=2)

        self.card_area = ctk.CTkScrollableFrame(self)
        self.card_area.grid(
            row=1, column=0, columnspan=3, sticky="nsew", padx=10, pady=(0, 10)
        )

        self.card_area.grid_columnconfigure(0, weight=1)
        self.card_area.grid_columnconfigure(1, weight=1)

        self.flashcard_frames = []

        self.add_card_button = ctk.CTkButton(
            self.card_area,
            image=self.icon_plus,
            text="",
            fg_color="transparent",
            hover_color="#C5F6FF",
            command=self.add_flashcard_frame,
        )

        for card in self.flashcards:
            self.add_flashcard_frame(card["front"], card["back"], card["card_id"])

        self.reposition_plus_icon()

        ctk.CTkButton(self, text="Save", command=self.save_set).grid(
            row=2, column=0, columnspan=3, pady=(10, 10)
        )

    def add_flashcard_frame(self, front_text="", back_text="", card_id=None):
        front_textbox = ctk.CTkTextbox(self.card_area, height=80, wrap="word")
        front_textbox.insert("1.0", front_text)
        front_textbox.grid(padx=(10, 5), pady=(5, 5), sticky="ew")

        back_textbox = ctk.CTkTextbox(self.card_area, height=80, wrap="word")
        back_textbox.insert("1.0", back_text)
        back_textbox.grid(padx=(5, 5), pady=(5, 5), sticky="ew")

        delete_button = ctk.CTkButton(
            self.card_area,
            image=self.icon_bin,
            text="",
            fg_color="transparent",
            hover_color="#FFD5D2",
            command=lambda: self.delete_flashcard_frame(
                (front_textbox, back_textbox, delete_button, card_id)
            ),
        )
        delete_button.grid(padx=(5, 10), pady=(5, 5), sticky="ns")

        self.flashcard_frames.append(
            (front_textbox, back_textbox, delete_button, card_id)
        )
        self.reposition_flashcard_frames()

    def delete_flashcard_frame(self, frame):
        front_textbox, back_textbox, delete_button, card_id = frame
        if card_id:
            self.deleted_card_ids.append(card_id)

        if frame in self.flashcard_frames:
            self.flashcard_frames.remove(frame)
            for widget in frame[:3]:
                widget.destroy()

        self.reposition_flashcard_frames()

    def reposition_flashcard_frames(self):
        for i, (front_textbox, back_textbox, delete_button, _) in enumerate(
            self.flashcard_frames
        ):
            front_textbox.grid(row=i, column=0, padx=(10, 5), pady=(5, 5), sticky="ew")
            back_textbox.grid(row=i, column=1, padx=(5, 5), pady=(5, 5), sticky="ew")
            delete_button.grid(row=i, column=2, padx=(5, 10), pady=(5, 5), sticky="ns")
        self.reposition_plus_icon()

    def reposition_plus_icon(self):
        plus_row = len(self.flashcard_frames)
        self.add_card_button.grid(
            row=plus_row, column=0, columnspan=2, pady=(10, 10), sticky="ew"
        )

    def save_set(self):
        updated_flashcards = []
        for front_textbox, back_textbox, _, card_id in self.flashcard_frames:
            front_text = front_textbox.get("1.0", "end").strip()
            back_text = back_textbox.get("1.0", "end").strip()
            if front_text and back_text:
                updated_flashcards.append(
                    {"front": front_text, "back": back_text, "card_id": card_id}
                )

        self.save_callback(self.set_name, updated_flashcards, self.deleted_card_ids)
        self.destroy()
