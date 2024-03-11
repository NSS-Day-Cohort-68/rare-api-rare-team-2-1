import sqlite3
import json


def create_comment(comment):
    """Adds a comment to the database when form is submitted

    Args:
        comment (dictionary): The dictionary passed to the create comment request

    Returns:
        json string: Contains the token of the newly created comment
    """

    with sqlite3.connect("./db.sqlite3") as conn:

        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute(
            """
        Insert into Comments (author_id, post_id, content) values (?, ?, ?)
        """,
            (
                comment["author_id"],
                comment["post_id"],
                comment["content"],
            ),
        )

        id = db_cursor.lastrowid

        return json.dumps({"token": id, "valid": True})
