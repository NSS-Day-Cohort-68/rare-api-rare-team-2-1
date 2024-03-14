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


def get_comments_by_post_id(postId):
    """Retrieves all comments associated with a postId

    Args:
        post Id (integer): The unique id of a post

    Returns:
        a list of comment instances
    """

    with sqlite3.connect("./db.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute(
            """
            SELECT
                id,
                content,
                created_on,
                user
            FROM (
                SELECT
                    c.id AS id,
                    c.content AS content,
                    c.created_on AS created_on,
                    u.username AS user
                FROM Comments c
                JOIN Users u 
                ON u.id = c.author_id
                WHERE c.post_id = ?
            ) AS subquery
            ORDER BY created_on DESC;
            """,
            (postId,),
        )
        query_results = db_cursor.fetchall()

        comments = []
        for row in query_results:
            comment = {
                "id": row["id"],
                "content": row["content"],
                "created_on": row["created_on"],
                "user": row["user"],
            }
            comments.append(comment)

        serialized_comments = json.dumps(comments)

    return serialized_comments


def delete_comment(pk):
    with sqlite3.connect("./db.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()
        # Write the SQL query to get the information you want
        db_cursor.execute(
            """
        DELETE FROM Comments WHERE id = ?
        """,
            (pk,),
        )
        number_of_rows_deleted = db_cursor.rowcount

    return True if number_of_rows_deleted > 0 else False
