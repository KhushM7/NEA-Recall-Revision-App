from typing import List, Dict, Any
from physics_app.utilities.server_utilities.make_request import make_request

GET_DUE_FLASHCARDS_ENDPOINT = "/get_due_flashcards"
SUBMIT_RATING_ENDPOINT = "/submit_rating"
CREATE_FLASHCARD_ENDPOINT = "/create_flashcard"
GET_FLASHCARDS_BY_SET_ENDPOINT = "/get_flashcards_by_set"
GET_SETS_ENDPOINT = "/get_sets"


class FlashcardHandler:
    def __init__(self, server_url: str):
        self.server_url = server_url

    def get_due_flashcards(self, user_id: int) -> List[Dict[str, Any]]:
        """Fetch flashcards due for review."""
        result = make_request(
            "GET", GET_DUE_FLASHCARDS_ENDPOINT, params={"user_id": user_id}
        )
        return result.get("flashcards", [])

    def get_flashcards_by_set(
        self, user_id: int, set_name: str
    ) -> List[Dict[str, Any]]:
        """Fetch flashcards by set name."""
        params = {"user_id": user_id, "set_name": set_name}
        result = make_request("GET", GET_FLASHCARDS_BY_SET_ENDPOINT, params=params)
        return result.get("flashcards", [])

    def get_sets(self, user_id: int) -> List[str]:
        """Fetch all flashcard sets for a user."""
        result = make_request("GET", GET_SETS_ENDPOINT, params={"user_id": user_id})
        return result.get("sets", [])

    def submit_rating(self, user_id: int, card_id: int, rating: str) -> Dict[str, Any]:
        """Submit a rating for a flashcard."""
        payload = {"user_id": user_id, "card_id": card_id, "rating": rating}
        result = make_request("POST", SUBMIT_RATING_ENDPOINT, payload=payload)
        return result

    def create_flashcard(self, user_id: int, flashcard_data: Dict[str, str]):
        """Create a new flashcard."""
        payload = {"user_id": user_id, "flashcard_data": flashcard_data}
        result = make_request("POST", CREATE_FLASHCARD_ENDPOINT, payload=payload)
        return result
