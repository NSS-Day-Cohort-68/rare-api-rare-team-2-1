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


class JSONServer(HandleRequests):

    def do_GET(self):
        response_body = ""
        url = self.parse_url(self.path)
        if url["requested_resource"] == "posts":
            if url["pk"] != 0:
                response_body = get_single_post(url["pk"])
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

            # If no specific username provided, return all users
            response_body = get_all_users()

            return self.response(response_body, status.HTTP_200_SUCCESS.value)

        if url["requested_resource"] == "myposts":
            # need to change this to pass in the userId
            response_body = get_posts_by_user_id(user_id)
            return self.response(response_body, status.HTTP_200_SUCCESS.value)

        return self.response(
            "404", status.HTTP_404_CLIENT_ERROR_RESOURCE_NOT_FOUND.value
        )


def main():
    host = ""
    port = 8088
    HTTPServer((host, port), JSONServer).serve_forever()


if __name__ == "__main__":
    main()
