import requests
from typing import Dict, Any, Optional

SERVER_URL = "http://127.0.0.1:5000"


def make_request(
    method: str,
    endpoint: str,
    payload: Optional[Dict[str, Any]] = None,
    headers: Optional[Dict[str, str]] = None,
    params: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    """
    Helper function to make an HTTP request and handle errors.

    :param method: The HTTP method to use (GET, POST, PUT, DELETE).
    :param endpoint: The API endpoint to hit.
    :param payload: The data to send in the request (for POST, PUT).
    :param headers: Optional headers to include in the request.
    :param params: Optional query parameters for GET requests.
    :return: The response JSON data if successful, or an error message.
    """
    url = SERVER_URL + endpoint
    try:
        response = requests.request(
            method, url, json=payload, headers=headers, params=params
        )
        response.raise_for_status()  # Raise an exception for HTTP errors
        return response.json()  # Return the JSON response
    except requests.RequestException as e:
        print(f"Error: An error occurred: {e}")
        return {"error": str(e)}
