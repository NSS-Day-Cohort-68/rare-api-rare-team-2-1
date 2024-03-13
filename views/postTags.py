import sqlite3
import json


def create_post_tags(post_id, tag_id):
    """Adds a post tag to the database"""

    with sqlite3.connect("./db.sqlite3") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute(
            """
            INSERT INTO PostTags (post_id, tag_id) VALUES (?, ?)
            """,
            (post_id, tag_id),
        )

        last_row_id = db_cursor.lastrowid

        return json.dumps({"token": last_row_id, "valid": True})
