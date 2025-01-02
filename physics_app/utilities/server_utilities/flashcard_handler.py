from typing import List, Dict, Any
from physics_app.utilities.server_utilities.make_request import make_request

GET_DUE_FLASHCARDS_ENDPOINT = "/get_due_flashcards"
SUBMIT_RATING_ENDPOINT = "/submit_rating"
CREATE_FLASHCARD_ENDPOINT = "/create_flashcard"
GET_FLASHCARDS_BY_SET_ENDPOINT = "/get_flashcards_by_set"
GET_SETS_ENDPOINT = "/get_sets"
DELETE_CARD_ENDPOINT = "/delete_card"
UPDATE_FLASHCARD_ENDPOINT = "/update_flashcard"
DELETE_SET_ENDPOINT = "/delete_set"


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

    def get_set_names_with_num_terms(self, user_id: int) -> Dict[str, int]:
        """Fetch all flashcard sets for a user with the number of terms in each set."""
        sets = self.get_sets(user_id)
        set_names_with_num_terms = {}
        for set_name in sets:
            flashcards = self.get_flashcards_by_set(user_id, set_name)
            num_terms = len(flashcards)
            set_names_with_num_terms[set_name] = num_terms
        return set_names_with_num_terms

    def delete_card(self, user_id: int, card_id: int):
        """Delete a flashcard set."""
        DELETE_CARD_ENDPOINT = "/delete_card"
        payload = {"user_id": user_id, "card_id": card_id}
        result = make_request("POST", DELETE_CARD_ENDPOINT, payload=payload)
        return result

    def delete_set(self, user_id: int, set_name: str):
        """Delete a flashcard set."""
        payload = {"user_id": user_id, "set_name": set_name}
        result = make_request("POST", "/delete_set", payload=payload)
        return result

    def update_set(
        self,
        user_id: int,
        set_name: str,
        updated_flashcards: List[Dict[str, str]],
    ):
        """Update an existing flashcard set."""
        for flashcard in updated_flashcards:
            self.update_flashcard(user_id, set_name, flashcard)

    def update_flashcard(self, user_id: int, flashcard: Dict[str, str]):
        """Update an existing flashcard."""
        payload = {"user_id": user_id, "flashcard": flashcard}
        result = make_request("POST", "/update_flashcard", payload=payload)
        return result
