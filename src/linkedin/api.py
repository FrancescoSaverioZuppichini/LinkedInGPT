import os
from functools import cache
from typing import Dict, TypedDict

import requests

from .schemas import *


class API:
    def __init__(self, token: str):
        self.token = token
        self.session = requests.Session()
        self._set_headers()
        self._set_hooks()

    def _set_headers(self):
        headers = {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json",
        }
        self.session.headers = headers

    def _set_hooks(self):
        self.session.hooks = {
            "response": lambda r, *args, **kwargs: r.raise_for_status()
        }

    @cache
    def get_me(self) -> UserProfile:
        return self.session.get("https://api.linkedin.com/v2/me").json()

    def create_post(self, body: Dict) -> CreatePostResponse:
        return self.session.post("https://api.linkedin.com/v2/ugcPosts", json=body)

    def register_upload(self, body: RegisterUploadBody) -> RegisterUploadResponse:
        return self.session.post(
            "https://api.linkedin.com/v2/assets?action=registerUpload", json=body
        ).json()

    def upload_image(self, file_path: str, upload_url: str) -> requests.Response:
        with open(file_path, "rb") as file:
            response = requests.put(
                upload_url, data=file, headers={"Authorization": f"Bearer {self.token}"}
            )
        return response

    @classmethod
    def from_env(cls):
        return cls(os.environ["LINKEDIN_TOKEN"])
