import customtkinter as ctk


class ChooseSetToReview(ctk.CTkToplevel):
    def __init__(self, parent, sets):
        super().__init__(parent)
        self.title("Choose Set to Review")
        self.geometry("300x200")
        self.chosen_set = None

        self.sets = sets
        self.create_widgets()

        self.grab_set()
        self.transient(parent)

    def create_widgets(self):
        scrollable_frame = ctk.CTkScrollableFrame(self)
        scrollable_frame.pack(fill="both", expand=True)

        for idx, set_name in enumerate(self.sets):
            button = ctk.CTkButton(
                scrollable_frame,
                text=set_name,
                command=lambda name=set_name: self.choose_set(name),
            )
            button.pack(pady=5, padx=10, fill="x")

    def choose_set(self, set_name):
        self.chosen_set = set_name
        self.destroy()

    def get_chosen_set(self):
        self.wait_window()
        return self.chosen_set
