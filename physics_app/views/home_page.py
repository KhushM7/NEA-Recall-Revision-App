import customtkinter as ctk
from tkinter import Toplevel, NW, Canvas
from PIL import Image, ImageDraw, ImageFont, ImageTk

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
from physics_app.views.dashboard_page import DashboardPage


class HomePage(ctk.CTkFrame):
    def __init__(
        self,
        parent,
        user_id,
        server_url,
        on_review=None,
        on_create_set=None,
        on_library=None,
        on_logout=None,
    ):
        super().__init__(parent, fg_color="white")

        # User Authentication and Username
        self.master = parent
        self.user_id = user_id
        self.master.configure(fg_color="white")
        parent.grid_rowconfigure(0, weight=0)
        parent.grid_rowconfigure(1, weight=1)
        parent.grid_columnconfigure((0, 1, 2, 3, 4), weight=1)
        self.user_auth = UserAuthentication(server_url)
        self.username = self.user_auth.get_username(user_id) or "User"
        self.on_review_click = on_review
        self.on_create_set_click = on_create_set
        self.on_library_click = on_library
        self.on_logout = on_logout

        # Icons Setup
        self.icon_folders, _ = setup_folder_icon()
        self.icon_calender_clock, _ = setup_calender_clock_icon()
        self.icon_calender_cancel, _ = setup_calender_cancel_icon()
        self.icon_plus, _ = setup_plus_icon()
        self.icon_settings, _ = setup_settings_icon()
        self.icon_logout, _ = setup_logout_icon()

        # Layout Configuration

        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=1)  # Give space to the dashboard

        # Placeholder for logo
        ctk.CTkLabel(parent, text="Logo Placeholder", width=100, height=100).grid(
            row=0, column=0, sticky="w", padx=20, pady=20
        )

        button_font = ctk.CTkFont(family="Open Sans", size=18)
        button_color = "#B6DCFE"  # Light blue background

        # Buttons
        self.create_main_button(
            "Your Library",
            self.icon_folders,
            1,
            button_font,
            button_color,
            self.on_library_click,
        )
        self.create_main_button(
            "Scheduled Review",
            self.icon_calender_clock,
            2,
            button_font,
            button_color,
            lambda: self.on_review_click("scheduled"),
        )
        self.create_main_button(
            "Create",
            self.icon_plus,
            3,
            button_font,
            button_color,
            self.on_create_set_click,
        )

        # User Menu Button
        self.user_menu_image = self.create_user_icon(self.username[0])
        self.user_menu_button = ctk.CTkButton(
            parent,
            image=self.user_menu_image,
            text="",
            width=50,
            height=50,
            fg_color="transparent",  # User button background
            hover=False,
            command=self.toggle_user_menu,
        )
        self.user_menu_button.grid(row=0, column=4, sticky="e", padx=10, pady=5)
        self.user_menu = None
        self.dashboard = DashboardPage(self.master, self.user_id)
        self.dashboard.grid(row=1, column=0, columnspan=5, sticky="nsew")

    def create_main_button(self, text, image, column, font, color, command=None):
        """Create a styled button for the main interface."""
        ctk.CTkButton(
            self.master,
            text=text,
            image=image,
            font=font,
            fg_color=color,
            text_color="black",
            hover_color="#145DA0",
            compound="left",  # Icon on the left, text on the right
            command=command,
        ).grid(row=0, column=column, sticky="ew", padx=10, pady=10)

    def create_user_icon(self, letter):
        """Generate a circular image with the first letter of the username."""
        canvas_size = 60  # Canvas size (larger than the circle)
        circle_size = 50  # Diameter of the circular button
        image = Image.new(
            "RGBA",
            (canvas_size, canvas_size),
            (255, 255, 255, 0),  # Transparent background
        )
        draw = ImageDraw.Draw(image)

        # Calculate offsets to center the circle
        offset = (canvas_size - circle_size) // 2

        # Draw circle
        draw.ellipse(
            (offset, offset, offset + circle_size, offset + circle_size), fill="#0E273C"
        )  # Circle color

        # Load font and calculate text size
        try:
            font = ImageFont.truetype("arial.ttf", 22)
        except OSError:
            font = ImageFont.load_default()
        bbox = draw.textbbox((0, 0), letter, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]

        # Center text within the circle
        text_position = (
            (canvas_size - text_width) // 2,
            (canvas_size - text_height) // 2 - 2,
        )
        draw.text(text_position, letter, font=font, fill="white")

        return ctk.CTkImage(light_image=image, size=(canvas_size, canvas_size))

    def toggle_user_menu(self):
        if self.user_menu:
            self.user_menu.destroy()
            self.user_menu = None
        else:
            self.show_user_menu()

    def show_user_menu(self):
        # Popup menu
        if self.user_menu:  # Prevent duplicate menus
            return

        self.user_menu = Toplevel(self)
        self.user_menu.overrideredirect(True)  # Remove window decorations

        # Configure window transparency
        self.user_menu.wm_attributes(
            "-transparentcolor", "#FFFFFF"
        )  # Transparency key color

        # Create a rounded corner image
        menu_width, menu_height = 200, 150
        radius = 20  # Radius for rounded corners
        rounded_image = Image.new("RGBA", (menu_width, menu_height), (255, 255, 255, 0))
        draw = ImageDraw.Draw(rounded_image)
        draw.rounded_rectangle(
            (0, 0, menu_width, menu_height),
            radius=radius,
            fill="#CDEDFD",  # Background color
        )

        # Convert to Tkinter image
        self.rounded_bg_image = ImageTk.PhotoImage(rounded_image)

        # Canvas to display the image as background
        canvas = Canvas(
            self.user_menu,
            width=menu_width,
            height=menu_height,
            bg="#FFFFFF",
            highlightthickness=0,
        )
        canvas.create_image(0, 0, image=self.rounded_bg_image, anchor=NW)
        canvas.place(x=0, y=0)  # Place the canvas in the background

        # Position the menu to align with the right edge of the main window
        button_y = self.user_menu_button.winfo_rooty()
        button_height = self.user_menu_button.winfo_height()
        window_x = self.winfo_rootx()  # Main window's x-position
        window_width = self.winfo_width()  # Main window's width

        x = window_x + window_width - menu_width - 10  # Align menu's right edge
        y = button_y + button_height + 5
        self.user_menu.geometry(f"{menu_width}x{menu_height}+{x}+{y}")

        button_font = ctk.CTkFont(size=14)

        # Username Label
        ctk.CTkLabel(
            self.user_menu,
            text=self.username,
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color="black",
            bg_color="#CDEDFD",
        ).place(x=10, y=10)

        # Settings Button
        settings_button = ctk.CTkButton(
            self.user_menu,
            text="Settings",
            image=self.icon_settings,
            font=button_font,
            fg_color="#CDEDFD",
            bg_color="#CDEDFD",
            hover_color="#D7FDF0",
            text_color="black",
            compound="left",
            width=180,
            height=30,
            corner_radius=10,
            command=lambda: print("Settings clicked"),
        )
        settings_button.place(x=10, y=50)

        # Log Out Button
        logout_button = ctk.CTkButton(
            self.user_menu,
            text="Log Out",
            image=self.icon_logout,
            font=button_font,
            hover_color="#D7FDF0",
            fg_color="#CDEDFD",
            bg_color="#CDEDFD",
            text_color="black",
            compound="left",
            width=180,
            height=30,
            corner_radius=10,
            command=self.on_logout,
        )
        logout_button.place(x=10, y=90)

        # Attach menu to main window
        self.attach_menu_to_window()

    def attach_menu_to_window(self):
        """Attach the user menu to the main window."""

        def update_menu_position():
            if not self.user_menu:  # Stop updating if menu is destroyed
                return

            # Get updated position of the main window
            window_x = self.winfo_rootx()
            window_y = self.winfo_rooty()
            window_width = self.winfo_width()

            # Get updated position of the button relative to the main window
            button_y = self.user_menu_button.winfo_rooty()
            button_height = self.user_menu_button.winfo_height()

            # Calculate new menu position
            menu_width = 200
            x = window_x + window_width - menu_width - 10  # Align menu's right edge
            y = button_y + button_height + 5
            self.user_menu.geometry(f"+{x}+{y}")

            # Schedule the next update
            self.after(50, update_menu_position)

        # Start updating the position
        update_menu_position()
