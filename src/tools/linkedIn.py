from pathlib import Path

import requests

from linkedin.user import User

def write_linkedin_post(user: User, content: str, media_url: str):
    file_path = f"media.{Path(media_url).suffix}"
    with open(file_path, "wb") as f:
        f.write(requests.get(media_url).content)
    user.create_post(
        content
        + "\n#opensource #llms #datascience #machinelearning #programming #ai #ds #python #deeplearning #nlp",
        [(file_path, "media")],
    )
    return "Post created! Good job!"