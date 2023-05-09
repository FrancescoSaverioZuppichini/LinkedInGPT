from typing import List

from src.types import Content


class ContentProvider:
    def get_contents(self) -> List[Content]:
        raise NotImplemented
