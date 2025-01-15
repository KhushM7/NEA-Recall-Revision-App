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


def setup_folder_icon():
    return setup_icon(OutlineIcon.FOLDERS, color="#000")


def setup_calender_clock_icon():
    return setup_icon(OutlineIcon.CALENDAR_CLOCK, color="#000")


def setup_calender_cancel_icon():
    return setup_icon(OutlineIcon.CALENDAR_CANCEL, color="#000")


def setup_plus_icon():
    return setup_icon(OutlineIcon.PLUS, color="#000")


def setup_bin_icon():
    return setup_icon(OutlineIcon.TRASH, color="#000")


def setup_settings_icon():
    return setup_icon(OutlineIcon.SETTINGS, color="#000")


def setup_logout_icon():
    return setup_icon(OutlineIcon.LOGOUT, color="#000")


def setup_info_icon():
    return setup_icon(OutlineIcon.INFO_CIRCLE, color="#000")


def setup_error_icon():
    return setup_icon(OutlineIcon.EXCLAMATION_CIRCLE, color="#d74141")


def setup_close_icon():
    return setup_icon(OutlineIcon.X, color="#000000")


def setup_show_password_icon():
    return setup_icon(OutlineIcon.EYE, color="#000000")


def setup_hide_password_icon():
    return setup_icon(OutlineIcon.EYE_OFF, color="#000000")


def setup_edit_icon():
    return setup_icon(OutlineIcon.EDIT, color="#000000")


def setup_next_icon():
    return setup_icon(OutlineIcon.CHEVRON_RIGHT, color="#000000")


def setup_previous_icon():
    return setup_icon(OutlineIcon.CHEVRON_LEFT, color="#000000")
