import sqlite3
import json


def create_category(category):
    """Adds a category to the database when they register

    Args:
        category (dictionary): The dictionary containing the category information

    Returns:
        json string: Contains the ID of the newly created category
    """
    with sqlite3.connect("./db.sqlite3") as conn:
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


def get_all_categories():
    """Gets categories"""
    # Open a connection to the database
    with sqlite3.connect("./db.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        # Write the SQL query to get the information you want
        db_cursor.execute(
            """
            SELECT
               id,
               label
            FROM Categories
            """
        )

        query_results = db_cursor.fetchall()

        # Initialize a list to hold categories
        categories = []

        # Iterate through query results and construct dictionaries for each category
        for row in query_results:
            category = {
                "id": row["id"],
                "label": row["label"],
            }
            categories.append(category)

        # Serialize Python list of users to JSON encoded string
        serialized_categories = json.dumps(categories)

        return serialized_categories


def delete_category(pk):
    with sqlite3.connect("./db.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        # Write the SQL query to get the information you want
        db_cursor.execute(
            """
        DELETE FROM Categories WHERE id = ?
        """,
            (pk,),
        )
        number_of_rows_deleted = db_cursor.rowcount

    return True if number_of_rows_deleted > 0 else False


def update_category(id, category_data):
    with sqlite3.connect("./db.sqlite3") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute(
            """
            UPDATE Categories
                SET
                    label = ?
            WHERE id = ?
            """,
            (category_data["label"], id),
        )

        rows_affected = db_cursor.rowcount

    return True if rows_affected > 0 else False
