from pytablericons import TablerIcons, OutlineIcon
import customtkinter as ctk


def setup_icon(icon_type, color, size=24, stroke_width=2):
    """
    Load and return an icon and its size as a CTkImage.

    :param icon_type: The type of icon to load (e.g., OutlineIcon.INFO_CIRCLE).
    :param color: The color of the icon.
    :param size: The size of the icon. Defaults to 24.
    :param stroke_width: The stroke width of the icon. Defaults to 2.
    :return: A tuple containing the CTkImage and size of the icon.
    """
    loaded_icon = TablerIcons.load(
        icon_type, size, color=color, stroke_width=stroke_width
    )
    icon_image = ctk.CTkImage(light_image=loaded_icon)
    return icon_image, size


def setup_info_icon():
    return setup_icon(OutlineIcon.INFO_CIRCLE, color="#000")


def setup_error_icon():
    return setup_icon(OutlineIcon.EXCLAMATION_CIRCLE, color="#d74141")


def setup_close_icon():
    return setup_icon(OutlineIcon.X, color="#000000")
