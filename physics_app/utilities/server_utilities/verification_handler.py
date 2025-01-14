from physics_app.utilities.server_utilities.make_request import make_request

SEND_VERIFICATION_CODE_ENDPOINT = "/send_verification_code"
VERIFY_OTP_ENDPOINT = "/verify_otp"


class VerificationHandler:
    def __init__(self, server_url: str):
        self.server_url = server_url

    def request_verification_code(self, email: str) -> bool:
        """
        Request a verification code for the given email.

        :param email: The email address to request the verification code for.
        :return: True if the verification code was sent successfully, False otherwise.
        """
        result = make_request("POST", SEND_VERIFICATION_CODE_ENDPOINT, {"email": email})
        return "error" not in result

    def request_verify_otp(self, email: str, otp: str) -> bool:
        """
        Verify the OTP for the given email.

        :param email: The email address associated with the OTP.
        :param otp: The OTP to verify.
        :return: True if the OTP was verified successfully, False otherwise.
        """
        result = make_request("POST", VERIFY_OTP_ENDPOINT, {"email": email, "otp": otp})
        return "error" not in result
