import customtkinter as ctk
from tkinter import Toplevel

from physics_app.utilities.server_utilities.user_authentication import (
    UserAuthentication,
)
from physics_app.utilities.setup_icons import (
    setup_folder_icon,
    setup_calender_clock_icon,
    setup_calender_cancel_icon,
    setup_plus_icon,
    setup_settings_icon,
    setup_logout_icon,
)


class HomePage(ctk.CTkFrame):
    def __init__(
        self, root, user_id, server_url, on_review_click=None, on_create_set_click=None
    ):
        super().__init__(root, fg_color="white")
        print(root.winfo_width())
        print(self.winfo_width())
        self.grid(sticky="nsew")
        self.user_auth = UserAuthentication(server_url)
        self.username = self.user_auth.get_username(user_id)
        self.on_review_click = on_review_click
        self.on_create_set_click = on_create_set_click
        self.icon_folders, self.icon_folders_size = setup_folder_icon()
        self.icon_calender_clock, self.icon_calender_clock_size = (
            setup_calender_clock_icon()
        )
        self.icon_calender_cancel, self.icon_calender_cancel_size = (
            setup_calender_cancel_icon()
        )
        self.icon_plus, self.icon_plus_size = setup_plus_icon()
        self.icon_settings, self.icon_settings_size = setup_settings_icon()
        self.icon_logout, self.icon_logout_size = setup_logout_icon()
        self.grid_columnconfigure((0, 1, 2, 3, 4, 5), weight=1)
        self.grid_rowconfigure(0, weight=0)
        # Placeholder for logo
        logo_placeholder = ctk.CTkLabel(
            self, text="Logo Placeholder", width=100, height=100
        )
        logo_placeholder.grid(row=0, column=0, sticky="w", padx=20, pady=20)

        # Library button with tooltip
        library_button = ctk.CTkButton(
            self,
            text="Your Library",
            image=self.icon_folders,
        )
        library_button.grid(row=0, column=1, sticky="w", padx=10)

        # Scheduled review button
        scheduled_review_button = ctk.CTkButton(
            self,
            text="Scheduled Review",
            image=self.icon_calender_clock,
            command=lambda: self.on_review_click("scheduled"),
        )
        scheduled_review_button.grid(row=0, column=2, sticky="w", padx=10)

        # Unscheduled review button
        unscheduled_review_button = ctk.CTkButton(
            self,
            text="Unscheduled Review",
            image=self.icon_calender_cancel,
            command=lambda: self.on_review_click("unscheduled"),
        )
        unscheduled_review_button.grid(row=0, column=3, sticky="w", padx=10)

        # Create set button ("+" icon)
        create_set_button = ctk.CTkButton(
            self,
            text="Create",
            image=self.icon_plus,
            command=self.on_create_set_click,
        )
        create_set_button.grid(row=0, column=4, padx=0)

        # User icon and menu
        # Create a circular user menu button
        letter = self.username[0]  # Get the first letter
        text_width = (
            len(letter) * 16
        )  # Estimate the width of the letter in pixels (16 is an average width)
        button_diameter = max(
            text_width, 40
        )  # Set a minimum diameter (e.g., 40px for single characters)

        self.user_menu_button = ctk.CTkButton(
            self,
            text=letter,  # Display the letter
            width=button_diameter,  # Button width matches diameter
            height=button_diameter,  # Button height matches diameter
            corner_radius=button_diameter // 2,  # Make it circular
            fg_color="blue",  # Button background color
            text_color="white",  # Letter color
            font=ctk.CTkFont(size=14, weight="bold"),  # Adjust font size as needed
            command=self.toggle_user_menu,  # Action when clicked
        )
        self.user_menu_button.grid(row=0, column=5, sticky="e", padx=10)

        self.user_menu = None

    def toggle_user_menu(self):
        if self.user_menu:
            self.user_menu.destroy()
            self.user_menu = None
        else:
            self.show_user_menu()

    def show_user_menu(self):
        self.user_menu = Toplevel(self)
        self.user_menu.overrideredirect(True)
        # x = self.user_menu_button.winfo_rootx() - 50
        # y = self.user_menu_button.winfo_rooty() + 50
        # self.user_menu.geometry(f"150x100+{x}+{y}")

        user_label = ctk.CTkLabel(self.user_menu, text=self.username)
        user_label.pack(pady=(10, 5))

        settings_button = ctk.CTkButton(
            self.user_menu,
            text="Settings",
            image=self.icon_settings,
            command=lambda: print("Settings clicked"),
        )
        settings_button.pack(fill="x", padx=10, pady=5)

        logout_button = ctk.CTkButton(
            self.user_menu,
            text="Log Out",
            image=self.icon_logout,
            command=lambda: print("Log Out clicked"),
        )
        logout_button.pack(fill="x", padx=10, pady=5)
