import requests
from typing import Dict, Any

SERVER_URL = "http://127.0.0.1:5000"
SEND_VERIFICATION_CODE_ENDPOINT = "/send_verification_code"
VERIFY_OTP_ENDPOINT = "/verify_otp"


def make_request(endpoint: str, payload: Dict[str, Any]) -> bool:
    """
    Helper function to make a POST request and handle errors.

    :param endpoint: The API endpoint to hit.
    :param payload: The data to send in the request.
    :return: True if the request was successful, False otherwise.
    """
    try:
        response = requests.post(SERVER_URL + endpoint, json=payload)
        if response.status_code == 200:
            return True
        else:
            error_message = response.json().get("error", "Unknown error occurred.")
            print(f"Error: {error_message}")
            return False
    except requests.RequestException as e:
        print(f"Error: An error occurred: {e}")
        return False


def request_verification_code(email: str) -> bool:
    """
    Request a verification code for the given email.

    :param email: The email address to request the verification code for.
    :return: True if the verification code was sent successfully, False otherwise.
    """
    return make_request(SEND_VERIFICATION_CODE_ENDPOINT, {"email": email})


def request_verify_otp(email: str, otp: str) -> bool:
    """
    Verify the OTP for the given email.

    :param email: The email address associated with the OTP.
    :param otp: The OTP to verify.
    :return: True if the OTP was verified successfully, False otherwise.
    """
    return make_request(VERIFY_OTP_ENDPOINT, {"email": email, "otp": otp})
