from typing import List

from src.types import Content


class Storage:
    def store(self, content: Content):
        raise NotImplemented

    def update(self, content: Content):
        raise NotImplemented

    def get_all(self) -> List[Content]:
        raise NotImplemented

    def close(self):
        raise NotImplemented
