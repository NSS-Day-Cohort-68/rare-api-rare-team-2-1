import json
from http.server import HTTPServer
from nss_handler import HandleRequests, status
from views import get_all_users, retrieve_user, retrieve_user_by_email, create_user


class JSONServer(HandleRequests):

    def do_GET(self):
        response_body = ""
        url = self.parse_url(self.path)

        if url["requested_resource"] == "users":
            if url["pk"] != 0:
                response_body = retrieve_user(url["pk"])
                return self.response(response_body, status.HTTP_200_SUCCESS.value)

            elif "email" in url["query_params"]:
                email = url["query_params"]["email"][0]
                response_body = retrieve_user_by_email(email)
                return self.response(response_body, status.HTTP_200_SUCCESS.value)

            response_body = get_all_users()
            return self.response(response_body, status.HTTP_200_SUCCESS.value)

        return self.response("", status.HTTP_404_CLIENT_ERROR_RESOURCE_NOT_FOUND.value)

    def do_POST(self):
        url = self.parse_url(self.path)
        content_len = int(self.headers.get("content-length", 0))
        request_body = self.rfile.read(content_len)
        request_body = json.loads(request_body)

        if url["requested_resource"] == "users":
            successfully_posted = create_user(request_body)
            if successfully_posted:
                return self.response("", status.HTTP_201_SUCCESS_CREATED.value)

        else:
            return self.response(
                "Not Found", status.HTTP_404_CLIENT_ERROR_RESOURCE_NOT_FOUND.value
            )

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
