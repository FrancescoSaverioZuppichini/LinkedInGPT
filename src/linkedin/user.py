from .api import API
from typing import Optional, List
from .schemas import *
from rich import print


class User:
    def __init__(self, api: API = None):
        self._api = API.from_env() if api is None else api
        self._me = self._api.get_me()

    def create_post(self, text: str, image_path: Optional[str] = None) -> bool:
        shareMediaCategory = "NONE" if image_path is None else "IMAGE"
        author = f"urn:li:person:{self._me['id']}"
        media: List[Media] = []
        if image_path:
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
            media = [
                Media(
                    status="READY",
                    description=Description(text="My Image"),
                    media=asset_id,
                    title=Title(text="My image title")
                )
            ]
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

        print(create_post_body)

        return self._api.create_post(create_post_body).json()
