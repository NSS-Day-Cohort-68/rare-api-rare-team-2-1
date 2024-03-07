import sqlite3
import json


def create_category(category):
    """Adds a category to the database when they register

    Args:
        category (dictionary): The dictionary containing the category information

    Returns:
        json string: Contains the ID of the newly created category
    """
    with sqlite3.connect("./rare-api-rare-team-2-1/db.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute(
            """
            INSERT INTO Categories (label) VALUES (?)
            """,
            (category["label"],),
        )

        id = db_cursor.lastrowid

        return json.dumps({"id": id})
