from dataclasses import dataclass
from typing import List, Optional, Tuple

from requests import Response
from rich import print

from .api import API
from .schemas import *


class User:
    def __init__(self, api: API = None):
        self._api = API.from_env() if api is None else api
        self._me = self._api.get_me()

    def _register_and_upload_image(self, image_path: str) -> str:
        author = f"urn:li:person:{self._me['id']}"
        register_upload_body = RegisterUploadBody(
            registerUploadRequest=RegisterUploadRequest(
                recipes=["urn:li:digitalmediaRecipe:feedshare-image"],
                owner=author,
                serviceRelationships=[
                    ServiceRelationship(
                        relationshipType="OWNER",
                        identifier="urn:li:userGeneratedContent",
                    )
                ],
            )
        )
        response = self._api.register_upload(register_upload_body)
        # [NOTE] LinkedIn apis have '.' in the name making it impossible to use TypeDicts
        upload_url = response["value"]["uploadMechanism"][
            "com.linkedin.digitalmedia.uploading.MediaUploadHttpRequest"
        ]["uploadUrl"]
        asset_id = response["value"]["asset"]
        response = self._api.upload_image(image_path, upload_url)

        return asset_id

    def create_post(
        self, text: str, images: Optional[List[Tuple[str, str]]] = None
    ) -> bool:
        """To create a post with the LinkedIn Apis we need to
         - (if we have an image): register the image upload, store the returned uploadUrl
         - (if we have an image): upload the image
         - send the post, (if we have an image) add the correct image to the `media` request body

        Args:
            text (str): _description_
            image_path (Optional[str], optional): _description_. Defaults to None.

        Returns:
            bool: _description_
        """
        shareMediaCategory = "NONE" if images is None else "IMAGE"
        author = f"urn:li:person:{self._me['id']}"
        media: List[Media] = []

        for image_path, image_description in images:
            asset_id = self._register_and_upload_image(image_path)
            media.append(
                Media(
                    status="READY",
                    description=Description(text=image_description),
                    media=asset_id,
                    title=Title(text="Image Title"),
                )
            )
        create_post_body = {
            "author": author,
            "lifecycleState": "PUBLISHED",
            "specificContent": {
                "com.linkedin.ugc.ShareContent": {
                    "shareCommentary": {"text": text},
                    "shareMediaCategory": shareMediaCategory,
                    "media": media,
                }
            },
            "visibility": {"com.linkedin.ugc.MemberNetworkVisibility": "PUBLIC"},
        }

        return self._api.create_post(create_post_body).json()
