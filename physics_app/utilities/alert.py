import customtkinter as ctk
from physics_app.utilities.setup_icons import setup_close_icon


class Alert(ctk.CTkFrame):
    def __init__(
        self,
        master=None,
        title="",
        message="",
        title_font=None,
        message_font=None,
        title_color="#000000",
        message_color="#000000",
        fg_color="#FFFFFF",
        icon=None,
        width=300,
        height=150,
        **kwargs
    ):
        super().__init__(
            master, width=width, height=height, fg_color=fg_color, **kwargs
        )
        self.title = title
        self.close_icon, self.close_icon_size = setup_close_icon()

        # Set default fonts if not provided
        title_font = title_font or ctk.CTkFont(size=14, weight="bold")
        message_font = message_font or ctk.CTkFont(size=12, weight="normal")

        # Title Label
        self.title_label = ctk.CTkLabel(
            self,
            text=self.title,
            text_color=title_color,
            font=title_font,
            fg_color=fg_color,
            anchor="w",
        )
        self.title_label.grid(row=0, column=1, padx=(10, 0), pady=(10, 0), sticky="w")

        # Message Label
        self.message_label = ctk.CTkLabel(
            self,
            text=message,
            text_color=message_color,
            font=message_font,
            fg_color=fg_color,
            justify="left",
            anchor="w",
        )
        self.message_label.grid(
            row=1, column=1, padx=(10, 0), pady=(0, 10), sticky="ew"
        )

        # Icon
        if icon:
            self.icon = ctk.CTkLabel(self, image=icon, fg_color=fg_color, text="")
            self.icon.grid(row=0, column=0, padx=(10, 0), pady=(10, 0), sticky="nw")

        # Close Button
        self.button = ctk.CTkButton(
            self,
            text="",
            image=self.close_icon,
            width=self.close_icon_size,
            fg_color=fg_color,
            hover=False,
            command=self.hide,
        )
        self.button.grid(row=0, column=2, padx=(0, 10), pady=(10, 0), sticky="ne")

        # Grid configuration
        self.grid_columnconfigure(0, weight=0)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=0)

        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=1)

    def show(self, row=0, column=0, padx=10, pady=None, columnspan=None, sticky="nsew"):
        self.grid(
            row=row,
            column=column,
            columnspan=columnspan,
            padx=padx,
            pady=pady,
            sticky=sticky,
        )

    def hide(self):
        self.grid_forget()

    def update_text(self, new_title: str, new_message: str):
        """Update the title and message text of the alert."""
        self.title_label.configure(text=new_title)
        self.message_label.configure(text=new_message)
