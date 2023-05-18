from pathlib import Path

import requests
from linkedin_python import User

from src.logger import logger
from src.types import GeneratedContent

from .base import Action


class PostOnLinkedInAction(Action):
    def __init__(self) -> None:
        self.user = User()

    def __call__(self, content: GeneratedContent):
        if content.media_url is not None:
            media_url = content.media_url
            if media_url.startswith("http"):
                file_path = f"media{Path(media_url).suffix}"
                with open(file_path, "wb") as f:
                    f.write(requests.get(media_url).content)
                media_url = file_path
            logger.debug(
                f"Creating LinkedIn post with text = {content.text} and media = {media_url}"
            )
            self.user.create_post(
                content.text,
                [(media_url, "media")],
            )
        else:
            logger.debug(f"Creating LinkedIn post with text = {content.text}")
            self.user.create_post(content.text)
