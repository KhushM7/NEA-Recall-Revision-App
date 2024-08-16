import requests

SERVER_URL = "http://127.0.0.1:5000"


def request_verification_code(email):
    try:
        response = requests.post(
            SERVER_URL + "/send_verification_code", json={"email": email}
        )
        if response.status_code == 200:
            return True
        else:
            error_message = response.json().get(
                "error", "Failed to send verification code."
            )
            print("Error", error_message)
            return False
    except requests.RequestException as e:
        print("Error", f"An error occurred: {e}")
        return False


# Utility function to verify OTP
def request_verify_otp(email, otp):
    try:
        response = requests.post(
            SERVER_URL + "/verify_otp", json={"email": email, "otp": otp}
        )
        if response.status_code == 200:
            return True
        else:
            error_message = response.json().get("error", "Failed to verify the code.")
            print("Error", error_message)
            return False
    except requests.RequestException as e:
        print("Error", f"An error occurred: {e}")
        return False
