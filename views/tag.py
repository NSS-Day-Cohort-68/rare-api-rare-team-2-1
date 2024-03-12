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
