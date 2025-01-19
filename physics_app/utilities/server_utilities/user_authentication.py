from typing import Optional

from physics_app.utilities.server_utilities.make_request import make_request

REGISTER_ENDPOINT = "/register"
LOGIN_ENDPOINT = "/login"
UPDATE_PASSWORD_ENDPOINT = "/update_password"
IS_EMAIL_TAKEN_ENDPOINT = "/is_email_taken"
IS_USERNAME_TAKEN_ENDPOINT = "/is_username_taken"
GET_USER_ID_ENDPOINT = "/get_user_id"
GET_USERNAME_ENDPOINT = "/get_username"
UPDATE_EMAIL_ENDPOINT = "/update_email"
UPDATE_USERNAME_ENDPOINT = "/update_username"
GET_EMAIL_ENDPOINT = "/get_email"


class UserAuthentication:
    def __init__(self, server_url: str):
        self.server_url = server_url

    def register_user(self, email: str, username: str, password: str) -> bool:
        """
        Register a new user by sending their details to the server.

        :param email: The email address of the user.
        :param username: The username of the user.
        :param password: The password of the user.
        :return: True if the user was registered successfully, False otherwise.
        """
        result = make_request(
            "POST",
            REGISTER_ENDPOINT,
            {"email": email, "username": username, "password": password},
        )
        return "error" not in result

    def login_user(self, email_username: str, password: str) -> bool:
        """
        Log in a user by sending their email/username and password to the server.

        :param email_username: The email address or username of the user.
        :param password: The password of the user.
        :return: True if login was successful, False otherwise.
        """
        result = make_request(
            "POST",
            LOGIN_ENDPOINT,
            {"email_username": email_username, "password": password},
        )
        return "error" not in result

    def update_password(self, email: str, new_password: str) -> bool:
        """
        Update the password for a user by sending the new password to the server.

        :param email: The email address of the user.
        :param new_password: The new password for the user.
        :return: True if the password was updated successfully, False otherwise.
        """
        result = make_request(
            "POST", UPDATE_PASSWORD_ENDPOINT, {"email": email, "password": new_password}
        )
        return "error" not in result

    def is_email_taken(self, email: str) -> bool:
        """
        Check if the email is already taken by querying the server.

        :param email: The email address to check.
        :return: True if the email is taken, False otherwise.
        """
        result = make_request("GET", IS_EMAIL_TAKEN_ENDPOINT, params={"email": email})
        return result.get("email_taken", False)

    def is_username_taken(self, username: str) -> bool:
        """
        Check if the username is already taken by querying the server.

        :param username: The username to check.
        :return: True if the username is taken, False otherwise.
        """
        result = make_request(
            "GET", IS_USERNAME_TAKEN_ENDPOINT, params={"username": username}
        )
        return result.get("username_taken", False)

    def get_user_id(self, email_or_username: str) -> Optional[int]:
        """
        Retrieve the user ID based on email or username.

        :param email_or_username: The email or username of the user.
        :return: User ID if found, otherwise None.
        """
        result = make_request(
            "GET", GET_USER_ID_ENDPOINT, params={"email_or_username": email_or_username}
        )
        return result.get("user_id") if "user_id" in result else None

    def get_username(self, user_id: int) -> Optional[str]:
        """
        Retrieve the username based on user ID.

        :param user_id: The ID of the user.
        :return: Username if found, otherwise None.
        """
        result = make_request("GET", GET_USERNAME_ENDPOINT, params={"user_id": user_id})
        return result.get("username") if "username" in result else None

    def get_email(self, user_id: int) -> Optional[str]:
        """
        Retrieve the email based on user ID.

        :param user_id: The ID of the user.
        :return: Email if found, otherwise None.
        """
        result = make_request("GET", GET_EMAIL_ENDPOINT, params={"user_id": user_id})
        return result.get("email") if "email" in result else None

    def update_email(self, user_id: int, new_email: str) -> bool:
        """
        Update the email for a user by sending the new email to the server.

        :param user_id: The ID of the user.
        :param new_email: The new email for the user.
        :return: True if the email was updated successfully, False otherwise.
        """
        result = make_request(
            "POST", UPDATE_EMAIL_ENDPOINT, {"user_id": user_id, "email": new_email}
        )
        return "error" not in result

    def update_username(self, user_id: int, new_username: str) -> bool:
        """
        Update the username for a user by sending the new username to the server.

        :param user_id: The ID of the user.
        :param new_username: The new username for the user.
        :return: True if the username was updated successfully, False otherwise.
        """
        result = make_request(
            "POST",
            UPDATE_USERNAME_ENDPOINT,
            {"user_id": user_id, "username": new_username},
        )
        return "error" not in result
