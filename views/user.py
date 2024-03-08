import sqlite3
import json
from datetime import datetime


def login_user(user):
    """Checks for the user in the database

    Args:
        user (dict): Contains the username and password of the user trying to login

    Returns:
        json string: If the user was found will return valid boolean of True and the user's id as the token
                     If the user was not found will return valid boolean False
    """

    with sqlite3.connect("./db.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute(
            """
            select id, username
            from Users
            where username = ?
            and password = ?
        """,
            (user["username"], user["password"]),
        )

        user_from_db = db_cursor.fetchone()

        if user_from_db is not None:
            response = {
                "valid": True,
                "token": user_from_db["id"],
                "id": user_from_db["id"],
                "username": user_from_db["username"],
            }
        else:
            response = {"valid": False}

        return json.dumps(response)


def create_user(user):
    """Adds a user to the database when they register

    Args:
        user (dictionary): The dictionary passed to the register post request

    Returns:
        json string: Contains the token of the newly created user
    """


    with sqlite3.connect("./db.sqlite3") as conn:

        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute(
            """
        Insert into Users (first_name, last_name, username, email, password, profile_image_url, bio, created_on, active) values (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
            (
                user["first_name"],
                user["last_name"],
                user["email"],
                user["username"],
                user["password"],
                user["profile_image_url"],
                user["bio"],
                user["created_on"],
                user["active"],
            ),
        )

        id = db_cursor.lastrowid

        return json.dumps({"token": id, "valid": True})


def get_all_users():
    """Gets users"""
    # Open a connection to the database
    with sqlite3.connect("./db.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        # Write the SQL query to get the information you want
        db_cursor.execute(
            """
            SELECT
                id,
                first_name,
                last_name,
                email,
                bio,
                username,
                password,
                profile_image_url,
                created_on,
                active
            FROM Users
            """
        )

        query_results = db_cursor.fetchall()

        # Initialize a list to hold users
        users = []

        # Iterate through query results and construct dictionaries for each user
        for row in query_results:
            user = {
                "id": row["id"],
                "first_name": row["first_name"],
                "last_name": row["last_name"],
                "email": row["email"],
                "bio": row["bio"],
                "username": row["username"],
                "password": row["password"],
                "profile_image_url": row["profile_image_url"],
                "created_on": row["created_on"],
                "active": row["active"],
            }
            users.append(user)

        # Serialize Python list of users to JSON encoded string
        serialized_users = json.dumps(users)

        return serialized_users


def retrieve_user(pk):
    # Open a connection to the database
    with sqlite3.connect("./db.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        # Execute the SQL query to retrieve the user with the given primary key
        db_cursor.execute(
            """
            SELECT
                u.id,
                u.first_name,
                u.last_name,
                u.email,
                u.bio,
                u.username,
                u.password,
                u.profile_image_url,
                u.created_on,
                u.active
            FROM Users u
            WHERE id = ?
            """,
            (pk,),
        )

        # Fetch the query results
        query_results = db_cursor.fetchone()

        # Check if query_results is not None
        if query_results is not None:
            # Convert query_results to dictionary
            user = {
                "id": query_results["id"],
                "first_name": query_results["first_name"],
                "last_name": query_results["last_name"],
                "email": query_results["email"],
                "bio": query_results["bio"],
                "username": query_results["username"],
                "password": query_results["password"],
                "profile_image_url": query_results["profile_image_url"],
                "created_on": query_results["created_on"],
                "active": query_results["active"],
            }
            # Serialize Python dictionary to a JSON encoded string
            serialized_user = json.dumps(user)
        else:
            # If no user found with the given primary key, return an empty JSON object
            serialized_user = "{}"

        return serialized_user



def retrieve_user_by_email(email):
    # Open a connection to the database
    with sqlite3.connect("db.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        # Execute the SQL query to retrieve the user with the given primary key
        db_cursor.execute(
            """
            SELECT
                u.id,
                u.first_name,
                u.last_name,
                u.email,
                u.bio,
                u.username,
                u.password,
                u.profile_image_url,
                u.created_on,
                u.active
            FROM Users u
            WHERE u.email = ?
            """,
            (email,),
        )

        # Fetch the query results
        query_results = db_cursor.fetchone()

        # Check if query_results is not None
        if query_results is not None:
            # Convert query_results to dictionary
            user = {
                "id": query_results["id"],
                "first_name": query_results["first_name"],
                "last_name": query_results["last_name"],
                "email": query_results["email"],
                "bio": query_results["bio"],
                "username": query_results["username"],
                "password": query_results["password"],
                "profile_image_url": query_results["profile_image_url"],
                "created_on": query_results["created_on"],
                "active": query_results["active"],
            }
            # Serialize Python dictionary to a JSON encoded string
            serialized_user = json.dumps(user)
        else:
            # If no user found with the given primary key, return an empty JSON object
            serialized_user = "{}"

        return serialized_user


def retrieve_user_by_username(username):
    # Open a connection to the database
    with sqlite3.connect("./rare-api-rare-team-2-1/db.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        # Execute the SQL query to retrieve the user by username
        db_cursor.execute(
            """
            SELECT *
            FROM Users
            WHERE username = ?
            """,
            (username,),
        )

        # Fetch the query results
        query_result = db_cursor.fetchone()

        # Check if a user was found
        if query_result is not None:
            # Construct a dictionary representing the user
            user = {
                "password": query_result["password"],
                "username": query_result["username"],
                # Add other user attributes as needed
            }
            return user
        else:
            # If no user found with the provided username, return None
            return None

