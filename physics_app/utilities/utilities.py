import requests

SERVER_URL = "http://127.0.0.1:5000/send_verification_code"


def request_verification_code(email="yohev16251@iteradev.com"):
    response = requests.post(SERVER_URL, json={"email": email})
    if response.status_code == 200:
        print("Verification code request successful.")
    else:
        print(f"Failed to request verification code: {response.json()}")
