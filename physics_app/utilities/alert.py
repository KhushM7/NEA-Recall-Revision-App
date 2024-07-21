import customtkinter as ctk


class Alert(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)
        self.message_label = ctk.CTkLabel(self)
        self.message_label.grid(row=0, column=0, padx=10, pady=10)
        self.grid_remove()

    def show(self, message, bg_color=None, text_color=None, font=None):
        if bg_color:
            self.configure(bg_color=bg_color)
        if text_color:
            self.message_label.configure(text_color=text_color)
        if font:
            self.message_label.configure(font=font)

        self.message_label.configure(text=message)
        self.grid(row=0, column=0, padx=10, pady=10, sticky="ew")

    def hide(self):
        self.grid_remove()
