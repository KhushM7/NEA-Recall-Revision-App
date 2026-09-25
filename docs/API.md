# Server API (client contract)

This is every HTTP call the Recall desktop app makes to the [Recall App Server](https://github.com/KhushM7/Recall-App-Server): what it sends, and which fields it reads back. It is derived from the client code in `physics_app/utilities/server_utilities/`. The server repository is the authority on server-side behaviour; this page records what the **app depends on**, so a change on either side can be checked against it.

## Conventions

- **Base URL:** `http://127.0.0.1:5000`, set by `SERVER_URL` in `make_request.py`.
- **GET** requests send their arguments as **query parameters**.
- **POST** requests send a **JSON body**.
- Replies are expected to be **JSON objects**.
- **Errors:** `make_request` treats any non-2xx status, connection failure or timeout as an error and returns `{"error": "<message>"}` to the caller instead of raising. So:
  - calls that return **success/failure** (marked *ok?* below) succeed exactly when the reply has no `"error"` key;
  - calls that **read a field** fall back to a default (`[]`, `0`, `False` or `None`) when the field is missing.
- `user_id` is the integer ID returned by `GET /get_user_id` after login.
- Rating values are the strings `"Again"`, `"Hard"`, `"Good"` and `"Easy"`.
- Month names are full English names as produced by `strftime("%B")`, e.g. `"September"`.

## Accounts — `UserAuthentication`

| Method | Endpoint | Sends | Client reads | Used by |
|---|---|---|---|---|
| POST | `/register` | `{email, username, password}` | *ok?* | Sign up |
| POST | `/login` | `{email_username, password}` | *ok?* — a wrong password must return a non-2xx status | Log in |
| POST | `/update_password` | `{email, password}` | *ok?* | Forgot password (final step) |
| GET | `/is_email_taken` | `email` | `email_taken: bool` (default `False`) | Sign up, Settings |
| GET | `/is_username_taken` | `username` | `username_taken: bool` (default `False`) | Sign up, Settings |
| GET | `/get_user_id` | `email_or_username` | `user_id: int` (default `None`) | After login |
| GET | `/get_username` | `user_id` | `username: str` (default `None`) | Avatar letter, user menu, Settings |
| GET | `/get_email` | `user_id` | `email: str` (default `None`) | Settings |
| POST | `/update_email` | `{user_id, email}` | *ok?* | Settings |
| POST | `/update_username` | `{user_id, username}` | *ok?* | Settings |

`/login` accepts either an email address or a username in `email_username`, and `/get_user_id` must resolve either form too.

## Email verification — `VerificationHandler`

| Method | Endpoint | Sends | Client reads | Used by |
|---|---|---|---|---|
| POST | `/send_verification_code` | `{email}` | *ok?* | Forgot password → Send Verification Code / Resend Email |
| POST | `/verify_otp` | `{email, otp}` | *ok?* — an invalid code must return a non-2xx status | Forgot password → Submit |

## Flashcards — `FlashcardHandler`

A **flashcard** object as the client uses it:

```json
{ "card_id": 12, "front": "Translate: recordar", "back": "To remember" }
```

The client reads `card_id`, `front` and `back`, and ignores any extra fields.

| Method | Endpoint | Sends | Client reads | Used by |
|---|---|---|---|---|
| GET | `/get_due_flashcards` | `user_id` | `flashcards: [flashcard]` (default `[]`) | Scheduled Review |
| GET | `/get_flashcards_by_set` | `user_id, set_name` | `flashcards: [flashcard]` (default `[]`) | Practice a set, Edit set, library card counts |
| GET | `/get_sets` | `user_id` | `sets: [str]` (default `[]`) | Library |
| POST | `/submit_rating` | `{user_id, card_id, rating}` | whole reply (not inspected) | Scheduled Review rating buttons |
| POST | `/create_flashcard` | `{user_id, flashcard_data: {set_name, front, back}}` | whole reply (not inspected) | Create, Import, adding a card in Edit set |
| POST | `/update_flashcard` | `{user_id, flashcard: {card_id, front, back}}` | whole reply (not inspected) | Edit set → Save |
| POST | `/delete_card` | `{user_id, card_id}` | whole reply (not inspected) | Edit set → Save (removed cards) |
| POST | `/delete_set` | `{user_id, set_name}` | whole reply (not inspected) | Library bin icon |

Notes:
- There is no "create set" endpoint. A set exists as soon as one card has that `set_name`.
- `/submit_rating` is where the server runs FSRS: it updates the card's difficulty and stability, logs the review and sets the next due date.
- Which cards `/get_due_flashcards` returns, and the daily review limit applied to them, are decided by the server.

## Statistics and settings — `FlashcardHandler`

| Method | Endpoint | Sends | Client reads | Used by |
|---|---|---|---|---|
| GET | `/get_review_log_by_month` | `user_id, month, year` | `review_log: {day: count}` | Dashboard → Review Log |
| GET | `/get_next_reviews_by_month` | `user_id, month, year` | `next_reviews: {day: count}` | Dashboard → Future Reviews |
| GET | `/get_all_current_card_states` | `user_id` | `card_states: {state_name: count}` | Dashboard → Current Card States |
| GET | `/get_total_lapses` | `user_id` | `total_lapses: int` (default `0`) | Dashboard → Current Card States |
| GET | `/get_stability_data` | `user_id` | `stability_data: {key: stability_in_days}` (keys unused) | Dashboard → Card Stability |
| GET | `/get_difficulty_data` | `user_id` | `difficulty_data: {key: difficulty}` (keys unused) | Dashboard → Card Difficulty |
| GET | `/get_current_ratings` | `user_id` | `current_ratings: {label: count}` | Dashboard → Last Card Ratings |
| GET | `/get_daily_review_limit` | `user_id` | `daily_review_limit: int` (default `0`) | Settings |
| POST | `/update_daily_review_limit` | `{user_id, new_limit}` | whole reply (not inspected) | Settings → Save |

Shape details the charts rely on:

- **`{day: count}`**: keys are day-of-month numbers (ints or numeric strings, since the client calls `int(day)`) for the requested month. Days without reviews can be left out.
- **`{state_name: count}`** and **`{label: count}`**: the keys become pie-chart labels as-is. The demo data uses states such as `"New"` and `"Review"`, and ratings `"Again"`, `"Hard"`, `"Good"`, `"Easy"` and `"Not Reviewed"`.
- **Stability and difficulty:** only the **values** are used, to build a histogram. Return at least one card; with an empty dictionary the histogram's bin calculation fails.
- The dashboard code calls `.values()` on these replies, so they must be **objects**. Returning a list, or an error, breaks that panel.

## Keeping this page accurate

When you add or change a call in `physics_app/utilities/server_utilities/`, update the matching table here in the same commit, and make the matching change in the server repository.
