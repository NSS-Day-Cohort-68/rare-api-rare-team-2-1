import sqlite3
import json

def get_all_posts():
    # Open a connection to the database
    with sqlite3.connect("./db.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        # Write the SQL query to get the information you want
        db_cursor.execute(
            """
        SELECT
            p.title,
            p.publication_date,
            p.image_url,
            p.content,
            p.approved
        FROM Posts p;
        """
        )
        query_results = db_cursor.fetchall()

        # Initialize an empty list and then add each dictionary to it
        posts = []
        for row in query_results:
            post = {
                'title': row['title'],
                'publication_date': row['publication_date'],
                'image_url': row['image_url'],
                'content': row['content'],
                'approved': row['approved']
            }
            posts.append(post)

        # Serialize Python list to JSON encoded string
        serialized_posts = json.dumps(posts)

    return serialized_posts


def get_single_post(pk):
    # Open a connection to the database
    with sqlite3.connect("./db.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        # Write the SQL query to get the information you want
        db_cursor.execute(
            """
        SELECT
            p.id,
            p.title,
            p.publication_date,
            p.image_url,
            p.content,
            p.approved
        FROM Posts p
        WHERE p.id = ?;
        """,
            (pk,),
        )
        query_result = db_cursor.fetchone()

        # Serialize Python list to JSON encoded string
        serialized_order = json.dumps(dict(query_result))

    return serialized_order
