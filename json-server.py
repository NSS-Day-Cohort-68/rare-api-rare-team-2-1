import json
from http.server import HTTPServer
from nss_handler import HandleRequests, status
from views import (
    get_all_users,
    retrieve_user,
    login_user,
    retrieve_user_by_username,
    get_posts_by_user_id,
)
from views import get_single_post, get_all_posts


from views import (
    get_all_users,
    retrieve_user,
    login_user,
    retrieve_user_by_username,
    get_posts_by_user_id,
    retrieve_user_by_email,
    create_user
)
from views import (
    get_single_post,
    get_all_posts,
    create_category,
    get_all_categories,
    delete_category,
    update_category,
)

class JSONServer(HandleRequests):

    def do_GET(self):

        response_body = ""
        url = self.parse_url(self.path)

        if url["requested_resource"] == "posts":
            if url["pk"] != 0:
                response_body = get_single_post(url["pk"])
                return self.response(response_body, status.HTTP_200_SUCCESS.value)

            elif "user_Id" in url["query_params"]:
                user_id = int(url["query_params"]["user_Id"][0])

                response_body = get_posts_by_user_id(user_id)
                return self.response(response_body, status.HTTP_200_SUCCESS.value)

            response_body = get_all_posts()
            return self.response(response_body, status.HTTP_200_SUCCESS.value)

        if url["requested_resource"] == "users":
            if "pk" in url:
                if url["pk"] != 0:
                    response_body = retrieve_user(url["pk"])
                    return self.response(response_body, status.HTTP_200_SUCCESS.value)
            if "query_params" in url and "username" in url["query_params"]:
                username = url["query_params"]["username"]
                # Ensure username is converted to string
                if isinstance(username[0], str):
                    # Retrieve user by username from your database or data source
                    user = retrieve_user_by_username(username[0])
                    if user is not None:
                        response_body = login_user(user)
                        return self.response(
                            response_body, status.HTTP_200_SUCCESS.value
                        )
                    else:
                        # If no user found with the provided username
                        return self.response(
                            "User not found",
                            status.HTTP_404_CLIENT_ERROR_RESOURCE_NOT_FOUND.value,
                        )
                else:
                    # If the username is not a string, return a response indicating an invalid request
                    return self.response(
                        "Invalid username format",
                        status.HTTP_400_CLIENT_ERROR_BAD_REQUEST_DATA.value,
                    )
            elif "email" in url["query_params"]:
              email = url["query_params"]["email"][0]
              response_body = retrieve_user_by_email(email)
              return self.response(response_body, status.HTTP_200_SUCCESS.value)
            # If no specific username provided, return all users

            response_body = get_all_users()

            return self.response(response_body, status.HTTP_200_SUCCESS.value)


        if url["requested_resource"] == "myposts":
            # need to change this to pass in the userId
            response_body = get_posts_by_user_id(1)
            return self.response(response_body, status.HTTP_200_SUCCESS.value)

        if url["requested_resource"] == "categories":
            response_body = get_all_categories()
            return self.response(response_body, status.HTTP_200_SUCCESS.value)


        return self.response(
            "404", status.HTTP_404_CLIENT_ERROR_RESOURCE_NOT_FOUND.value
        )

    def do_POST(self):
        """Handle POST requests from a client"""

        url = self.parse_url(self.path)
        pk = url["pk"]


        content_len = int(self.headers.get("content-length", 0))
        request_body = self.rfile.read(content_len)
        request_body = json.loads(request_body)


        if url["requested_resource"] == "users":
            successfully_posted = create_user(request_body)
            if successfully_posted:
                return self.response("", status.HTTP_201_SUCCESS_CREATED.value)


        elif url["requested_resource"] == "categories":
            if pk == 0:
                successfully_posted = create_category(request_body)
                if successfully_posted:
                    return self.response("", status.HTTP_201_SUCCESS_CREATED.value)

                return self.response(
                    "Requested resource not found",
                    status.HTTP_404_CLIENT_ERROR_RESOURCE_NOT_FOUND.value,
                )

        else:
            return self.response(
                "Not found", status.HTTP_404_CLIENT_ERROR_RESOURCE_NOT_FOUND.value
            )

    def do_DELETE(self):
        """Handle DELETE requests from a client"""

        url = self.parse_url(self.path)
        pk = url["pk"]

        if url["requested_resource"] == "categories":
            if pk != 0:
                successfully_deleted = delete_category(pk)
                if successfully_deleted:
                    return self.response(
                        "", status.HTTP_204_SUCCESS_NO_RESPONSE_BODY.value
                    )

            return self.response(
                "Requested resource not found",
                status.HTTP_404_CLIENT_ERROR_RESOURCE_NOT_FOUND.value,
            )

    def do_PUT(self):
        """Handle PUT requests from a client"""

        # Parse the URL and get the primary key
        url = self.parse_url(self.path)
        pk = url["pk"]

        # Get the request body JSON for the new data
        content_len = int(self.headers.get("content-length", 0))
        request_body = self.rfile.read(content_len)
        request_body = json.loads(request_body)

        if url["requested_resource"] == "categories":
            if pk != 0:
                successfully_updated = update_category(pk, request_body)
                if successfully_updated:
                    return self.response(
                        "", status.HTTP_204_SUCCESS_NO_RESPONSE_BODY.value
                    )


def main():
    host = ""
    port = 8088
    HTTPServer((host, port), JSONServer).serve_forever()


if __name__ == "__main__":
    main()
