import sqlite3
import json
from datetime import datetime


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
        Insert into Comments (author_id, post_id, content, created_on) 
        VALUES (?, ?, ?, ?)
        """,
            (
                comment["author_id"],
                comment["post_id"],
                comment["content"],
                datetime.now().isoformat(),
            ),
        )

        id = db_cursor.lastrowid

        return json.dumps({"token": id, "valid": True})
