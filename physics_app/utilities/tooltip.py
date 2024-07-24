import tkinter as tk
from tkinter import ttk
import customtkinter as ctk


class Tooltip:
    def __init__(self, widget, text, hover_delay=1000):
        self.widget = widget
        self.text = text
        self.hover_delay = hover_delay
        self.tip_window = None
        self.widget.bind("<Enter>", self.on_enter)
        self.widget.bind("<Leave>", self.on_leave)

    def on_enter(self, event=None):
        self.schedule()

    def on_leave(self, event=None):
        self.unschedule()
        self.hide_tip()

    def schedule(self):
        self.unschedule()
        self._after_id = self.widget.after(self.hover_delay, self.show_tip)

    def unschedule(self):
        after_id = getattr(self, "_after_id", None)
        if after_id:
            self.widget.after_cancel(after_id)
            self._after_id = None

    def show_tip(self, event=None):
        if self.tip_window or not self.text:
            return
        x, y, _, _ = self.widget.bbox("insert")
        x += self.widget.winfo_rootx() + 43
        y += self.widget.winfo_rooty() + 25
        self.tip_window = tw = ctk.CTkToplevel(
            self.widget,
            fg_color="white",
        )
        tw.overrideredirect(True)
        tw.geometry("+%d+%d" % (x, y))

        label = ctk.CTkLabel(
            tw,
            text=self.text,
            font=ctk.CTkFont(size=10),
            fg_color="black",
            text_color="white",
            corner_radius=7,
            padx=4,
            pady=4,
        )
        label.pack(padx=4, pady=4)

    def hide_tip(self):
        tw = self.tip_window
        self.tip_window = None
        if tw:
            tw.destroy()
