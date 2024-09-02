import customtkinter as ctk
from typing import Optional, Tuple


class Tooltip:
    def __init__(
        self,
        widget: ctk.CTkLabel,
        text: str,
        hover_delay: int = 1000,
        font: Optional[ctk.CTkFont] = None,
        foreground_color: str = "black",
        background_color: str = "white",
        corner_radius: int = 7,
        win_padx: int = 10,
        win_pady: int = 25,
        padx: int = 4,
        pady: int = 4,
    ):
        self.widget = widget
        self.text = text
        self.hover_delay = hover_delay
        self.font = font or ctk.CTkFont(size=10)
        self.foreground_color = foreground_color
        self.background_color = background_color
        self.corner_radius = corner_radius
        self.win_padx = win_padx
        self.win_pady = win_pady
        self.padx = padx
        self.pady = pady
        self.tip_window = None
        self._after_id = None

        # Bind events to widget
        self.widget.bind("<Enter>", self.on_enter)
        self.widget.bind("<Leave>", self.on_leave)

    def on_enter(self, event=None):
        self.schedule()

    def on_leave(self, event=None):
        self.unschedule()
        self.hide_tip()

    def schedule(self):
        """Schedule the tooltip to show after the delay."""
        self.unschedule()  # Ensure any previous schedule is canceled
        self._after_id = self.widget.after(self.hover_delay, self.show_tip)

    def unschedule(self):
        """Cancel the scheduled tooltip display if any."""
        if self._after_id:
            self.widget.after_cancel(self._after_id)
            self._after_id = None

    def show_tip(self):
        """Create and display the tooltip."""
        if self.tip_window or not self.text:
            return

        # Get the position of the widget to place the tooltip
        x, y, _, _ = self.widget.bbox("insert")
        x += self.widget.winfo_rootx() + self.win_padx
        y += self.widget.winfo_rooty() + self.win_pady

        # Create tooltip window
        self.tip_window = ctk.CTkToplevel(self.widget, fg_color=self.background_color)
        self.tip_window.overrideredirect(True)
        self.tip_window.geometry(f"+{x}+{y}")

        # Create label for tooltip
        label = ctk.CTkLabel(
            self.tip_window,
            text=self.text,
            font=self.font,
            fg_color=self.foreground_color,
            text_color=self.background_color,
            corner_radius=self.corner_radius,
            padx=self.padx,
            pady=self.pady,
        )
        label.pack(padx=self.padx, pady=self.pady)

    def hide_tip(self):
        """Hide and destroy the tooltip window."""
        if self.tip_window:
            self.tip_window.destroy()
            self.tip_window = None
