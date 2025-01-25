import customtkinter as ctk
import tkinter as tk

from physics_app.utilities.setup_icons import (
    setup_show_password_icon,
    setup_hide_password_icon,
)


class PasswordEntry(ctk.CTkFrame):
    def __init__(self, master=None, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.configure(fg_color="#F1F2F3")

        self.icon_show_password, self.icon_show_password_size = (
            setup_show_password_icon()
        )
        self.icon_hide_password, self.icon_hide_password_size = (
            setup_hide_password_icon()
        )

        # Create password entry with *'s to hide the password
        self.password_entry = ctk.CTkEntry(self, show="*", placeholder_text="Password")
        self.password_entry.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Create toggle button with initial hide icon
        self.toggle_button = ctk.CTkButton(
            self,
            text="",
            command=self.toggle_password_visibility,
            image=self.icon_hide_password,
            width=self.icon_hide_password_size,
            height=self.icon_hide_password_size,
            fg_color="#F1F2F3",
            hover=False,
        )
        self.toggle_button.pack(side=tk.RIGHT)

        self.is_password_visible = False

    def toggle_password_visibility(self):
        if self.is_password_visible:
            self.password_entry.configure(show="*")
            self.toggle_button.configure(image=self.icon_hide_password)
        else:
            self.password_entry.configure(show="")
            self.toggle_button.configure(image=self.icon_show_password)

        self.is_password_visible = not self.is_password_visible

    def clear_entry(self):
        current_content = self.password_entry.get()
        if current_content:
            self.password_entry.delete(0, tk.END)
            self.password_entry.configure(placeholder_text="Password")
            self.is_password_visible = False
            self.toggle_button.configure(image=self.icon_hide_password)

    def get_entry(self):
        return self.password_entry.get()
