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


def get_tags_by_post_id(post_id):
    """GETs tags based on post Id"""

    with sqlite3.connect("./db.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute(
            """
            SELECT
                t.label AS tag_label
            FROM Tags t
            INNER JOIN PostTags pt ON t.id = pt.tag_id
            WHERE pt.post_id = ?;
            """,
            (post_id,),
        )
        query_results = db_cursor.fetchall()

        tags = []
        for row in query_results:
            tag = {
                "label": row["tag_label"],
            }
            tags.append(tag)

        serialized_tags = json.dumps(tags)

    return serialized_tags


def get_all_tags():
    """GETs all tags"""

    with sqlite3.connect("./db.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute(
            """
            SELECT
                *
            FROM Tags t
            """
        )
        query_results = db_cursor.fetchall()

        tags = []
        for row in query_results:
            tag = {
                "id": row["id"],
                "label": row["label"],
            }
            tags.append(tag)

        serialized_tags = json.dumps(tags)

    return serialized_tags


def delete_tag(pk):
    """Deletes a tag from the database

    Args:
        tag id (primary key): The unique id of a tag

    Returns:
        No content
    """
    with sqlite3.connect("./db.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        # Write the SQL query to get the information you want
        db_cursor.execute(
            """
        DELETE FROM Tags WHERE id = ?
        """,
            (pk,),
        )
        number_of_rows_deleted = db_cursor.rowcount

    return True if number_of_rows_deleted > 0 else False


def update_tag(id, tag_data):
    if not isinstance(tag_data, dict):
        raise ValueError("tag_data must be a dictionary")

    label = tag_data.get("label")
    if label is None:
        raise ValueError("tag_data must contain 'label' key")

    with sqlite3.connect("./db.sqlite3") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute(
            """
            UPDATE Tags
                SET
                    label = ?
            WHERE id = ?
            """,
            (label, id),
        )

        rows_affected = db_cursor.rowcount

    return rows_affected > 0
