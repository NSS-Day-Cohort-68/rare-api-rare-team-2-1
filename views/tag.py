import sqlite3
import json


def create_tag(tag):
    """Adds a tag to the database"""

    with sqlite3.connect("./db.sqlite3") as conn:

        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute(
            """
        INSERT INTO Tags (label) values (?)
        """,
            (tag["label"],),
        )

        last_row_id = db_cursor.lastrowid

        return json.dumps({"token": last_row_id, "valid": True})
