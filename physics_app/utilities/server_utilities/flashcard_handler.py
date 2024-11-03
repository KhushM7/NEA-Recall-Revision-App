from typing import List, Dict, Any
from physics_app.utilities.server_utilities.make_request import make_request

GET_DUE_FLASHCARDS_ENDPOINT = "/get_due_flashcards"
SUBMIT_RATING_ENDPOINT = "/submit_rating"


class FlashcardHandler:
    def __init__(self, server_url: str):
        self.server_url = server_url

    def get_due_flashcards(self, user_id: int) -> List[Dict[str, Any]]:
        """Fetch flashcards due for review."""
        result = make_request(
            "GET", GET_DUE_FLASHCARDS_ENDPOINT, params={"user_id": user_id}
        )
        return result.get("flashcards", [])

    def submit_rating(self, user_id: int, card_id: int, rating: str) -> Dict[str, Any]:
        """Submit a rating for a flashcard."""
        payload = {"user_id": user_id, "card_id": card_id, "rating": rating}
        result = make_request("POST", SUBMIT_RATING_ENDPOINT, payload=payload)
        return result
