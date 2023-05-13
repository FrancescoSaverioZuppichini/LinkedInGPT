from pathlib import Path

from linkedin_python import User

from src.types import GeneratedContent

from .base import Action


class PostOnLinkedInAction(Action):
    def __init__(self) -> None:
        self.user = User()

    def __call__(self, content: GeneratedContent):
        if content.media_url is not None:
            media_url = content.media_url
            if media_url.startswith("http"):
                media_url = f"media.{Path(media_url).suffix}"
            self.user.create_post(
                content.text,
                [(media_url, "media")],
            )
        else:
            self.user.create_post(content.text)
