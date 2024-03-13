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
                "title": row["title"],
                "publication_date": row["publication_date"],
                "image_url": row["image_url"],
                "content": row["content"],
                "approved": row["approved"],
            }
            posts.append(post)

        # Serialize Python list to JSON encoded string
        serialized_posts = json.dumps(posts)

    return serialized_posts


def get_posts_by_user_id(user_id):
    with sqlite3.connect("./db.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute(
            """
        SELECT
            p.id,
            p.title AS post_title,
            u.username AS author,
            c.label AS category
        FROM Posts p
        INNER JOIN Users u ON p.user_id = u.id
        INNER JOIN Categories c ON p.category_id = c.id
        WHERE p.user_id = ?;
        """,
            (user_id,),
        )
        query_results = db_cursor.fetchall()

        posts = []
        for row in query_results:
            post = {
                "id": row["id"],
                "title": row["post_title"],
                "author": row["author"],
                "category": row["category"],
            }
            posts.append(post)

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
                p.approved,
                u.username AS author_username
            FROM Posts p
            JOIN Users u ON p.user_id = u.id
            WHERE p.id = ?;
        """,
            (pk,),
        )
        query_result = db_cursor.fetchone()

        # Serialize Python list to JSON encoded string
        serialized_order = json.dumps(dict(query_result))

    return serialized_order


def get_all_posts_with_user_and_category():
    # Open a connection to the database
    with sqlite3.connect("./db.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        # Write the SQL query to get the information you want with joins
        db_cursor.execute(
            """
            SELECT
                p.id,
                p.title,
                p.publication_date,
                p.image_url,
                p.content,
                p.approved,
                u.username AS author_username,
                c.label AS category_name
            FROM Posts p
            LEFT JOIN Users u ON p.user_id = u.id
            LEFT JOIN Categories c ON p.category_id = c.id;
            """
        )
        query_results = db_cursor.fetchall()

        posts = []
        for row in query_results:
            post = {
                "id": row["id"],
                "title": row["title"],
                "author": row["author_username"],
                "category": row["category_name"],
                "content": row["content"],
            }
            posts.append(post)

        serialized_posts = json.dumps(posts)

    return serialized_posts


def delete_post(pk):
    """Adds a post to the database

    Args:
        post (dictionary): The dictionary containing the post information including category_id and user_id

    Returns:
        json string: Contains the ID of the newly created post
    """
    with sqlite3.connect("./db.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        # Write the SQL query to get the information you want
        db_cursor.execute(
            """
        DELETE FROM Posts WHERE id = ?
        """,
            (pk,),
        )
        number_of_rows_deleted = db_cursor.rowcount

    return True if number_of_rows_deleted > 0 else False


def create_post(post):
    """Adds a post to the database

    Args:
        post (dictionary): The dictionary containing the post information including category_id and user_id

    Returns:
        json string: Contains the ID of the newly created post
    """
    with sqlite3.connect("./db.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute(
            """
            INSERT INTO Posts (title, publication_date, image_url, content, approved, category_id, user_id) 
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (
                post["title"],
                post["publication_date"],
                post["image_url"],
                post["content"],
                post["approved"],
                post["category_id"],
                post["user_id"],
            ),
        )

        id = db_cursor.lastrowid

        return json.dumps({"id": id})

def update_post(post):
    """Updates a post in the database

    Args:
        post (dictionary): The dictionary containing the post information including category_id and user_id

    Returns:
        json string: Contains the ID of the updated post
    """
    with sqlite3.connect("./db.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute(
            """
            UPDATE Posts 
            SET title = ?, 
                publication_date = ?, 
                image_url = ?, 
                content = ?, 
                approved = ?, 
                category_id = ? 
            WHERE id = ?;
            """,
            (
                post["title"],
                post["publication_date"],
                post["image_url"],
                post["content"],
                post["approved"],
                post["category_id"],
                post["id"],  # Specify the ID of the post to update
            ),
        )

        return json.dumps({"id": post["id"]})
