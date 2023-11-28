import json
import os
import random
import urllib.error
import urllib.parse
import urllib.request
from typing import Dict, Tuple, Union, List

from dotenv import load_dotenv, find_dotenv
from faker import Faker

load_dotenv(find_dotenv())
Response_OBJ = Tuple[Union[Dict, List, str, None], int]
Fake = Faker()


class RequestClient:
    _time_out = 10

    _HEADERS = {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
    }

    def __init__(self, token: str = None):
        if token:
            self._HEADERS.update({'Authorization': f'Bearer {token}'})

    def get(self, url: str, headers: Dict = None) -> Response_OBJ:
        if headers:
            self._HEADERS.update(headers)
        request = urllib.request.Request(url, method='GET', headers=self._HEADERS)
        return self._make_request(request)

    def post(self, url: str, data: bytes, headers: Dict = None) -> Response_OBJ:
        if headers:
            self._HEADERS.update(headers)

        request = urllib.request.Request(url, data=data, headers=self._HEADERS, method='POST')
        return self._make_request(request)

    def _make_request(self, request: urllib.request.Request) -> Response_OBJ:
        try:
            with urllib.request.urlopen(request, timeout=self._time_out) as response:
                response_body = response.read()
                response_body = json.loads(response_body.decode('utf-8')) if response_body else None
                return response_body, response.status

        except urllib.error.HTTPError as http_err:
            error_message = f"HTTP error occurred: {http_err}"

        except urllib.error.URLError as url_err:
            if isinstance(url_err.reason, TimeoutError):
                error_message = f"Timeout error occurred: {url_err.reason}"
            else:
                error_message = f"Connection error occurred: {url_err.reason}"

        except Exception as req_err:
            error_message = f"Error sending data: {req_err}", req_err

        raise Exception(error_message)


if __name__ == '__main__':
    config = {
        "number_of_users": 4,
        "max_posts_per_user": 1,
        "max_likes_per_user": 5,
    }

    admin_token = os.getenv("TOKEN")
    print(admin_token)
    r = RequestClient()
    headers = {"Authorization": f"Bearer {admin_token}"}
    url = "http://127.0.0.1:8000"

    posts = []

    for _ in range(config.get("number_of_users")):
        UserData = {
            "email": Fake.email(),
            "first_name": Fake.first_name(),
            "last_name": Fake.last_name(),
            "password": Fake.password(length=10, special_chars=True, digits=True, upper_case=True, lower_case=True),
            "bio": Fake.text(max_nb_chars=100),
            "phone": "+380000000000",
        }
        response, status = r.post(f"{url}/api/sign-up/", data=json.dumps(UserData).encode('utf-8'), headers=headers)
        print(response, status)
        user_id = response.get("id")
        for _ in range(config.get("max_posts_per_user")):
            PostData = {
                # "photo": Fake.image_url(),
                "location": Fake.address(),
                "caption": Fake.text(),
                "title": Fake.text(max_nb_chars=50),
            }

            response, status = r.post(f"{url}/api/post/", data=json.dumps(PostData).encode('utf-8'), headers=headers)
            print(response, status)
            posts.append(response.get("id"))

    for _ in range(config.get("max_likes_per_user")):
        response, status = r.post(f"{url}/api/post/{random.choice(posts)}/like_post/", data=b'', headers=headers)
        print(response, status)
