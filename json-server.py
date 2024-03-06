import json
from http.server import HTTPServer
from nss_handler import HandleRequests, status
from views import get_all_users, retrieve_user, login_user, retrieve_user_by_username


class JSONServer(HandleRequests):

    def do_GET(self):
        response_body = ""
        url = self.parse_url(self.path)

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

        return self.response("", status.HTTP_404_CLIENT_ERROR_RESOURCE_NOT_FOUND.value)

    # def do_POST(self):
    #     url = self.parse_url(self.path)
    #     content_len = int(self.headers.get("content-length", 0))
    #     request_body = self.rfile.read(content_len)
    #     request_body = json.loads(request_body)

    #     if url["requested_resource"] == "users":
    #         successfully_posted = create_user(request_body)
    #         if successfully_posted:
    #             return self.response("", status.HTTP_201_SUCCESS_CREATED.value)

    #     else:
    #         return self.response(
    #             "Not Found", status.HTTP_404_CLIENT_ERROR_RESOURCE_NOT_FOUND.value
    #         )

    # def do_DELETE(self):
    #     url = self.parse_url(self.path)
    #     pk = url["pk"]

    #     if url["requested_resource"] == "users":
    #         if pk != 0:
    #             successfully_deleted = delete_user(pk)
    #             if successfully_deleted:
    #                 return self.response(
    #                     "", status.HTTP_204_SUCCESS_NO_RESPONSE_BODY.value
    #                 )

    #             return self.response(
    #                 "Requested resource not found",
    #                 status.HTTP_404_CLIENT_ERROR_RESOURCE_NOT_FOUND.value,
    #             )
    #         else:
    #             return self.response(
    #                 "Not found", status.HTTP_404_CLIENT_ERROR_RESOURCE_NOT_FOUND.value
    #             )

    # def do_PUT(self):
    #     url = self.parse_url(self.path)
    #     pk = url["pk"]

    #     content_len = int(self.headers.get("content-length", 0))
    #     request_body = self.rfile.read(content_len)
    #     request_body = json.loads(request_body)

    #     if url["requested_resource"] == "users":
    #         if "metals" and "price" in request_body:
    #             if pk != 0:
    #                 successfully_updated = update_user(pk, request_body)
    #                 if successfully_updated:
    #                     return self.response(
    #                         "", status.HTTP_204_SUCCESS_NO_RESPONSE_BODY.value
    #                     )
    #         else:
    #             return self.response(
    #                 "Missing required keys in the request body",
    #                 status.HTTP_400_CLIENT_ERROR_BAD_REQUEST_DATA.value,
    #             )
    #     return self.response(
    #         "Requested resource not found",
    #         status.HTTP_404_CLIENT_ERROR_RESOURCE_NOT_FOUND.value,
    #     )


def main():
    host = ""
    port = 8088
    HTTPServer((host, port), JSONServer).serve_forever()


if __name__ == "__main__":
    main()
