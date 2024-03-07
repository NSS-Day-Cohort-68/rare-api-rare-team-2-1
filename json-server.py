import json
from http.server import HTTPServer
from nss_handler import HandleRequests, status
from views import get_single_post, get_all_posts
from views import get_all_users, retrieve_user, get_all_posts, get_posts_by_user_id


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
            if url["pk"] != 0:
                response_body = retrieve_user(url["pk"])
                return self.response(response_body, status.HTTP_200_SUCCESS.value)

            response_body = get_all_users()

            return self.response(response_body, status.HTTP_200_SUCCESS.value)

        if url["requested_resource"] == "myposts":
            # need to change this to pass in the userId
            response_body = get_posts_by_user_id(1)
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
