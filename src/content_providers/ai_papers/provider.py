from typing import List

from src.types import Content

from ..base import ContentProvider
from .papers_with_code import get_latest_papers_from_papers_with_code


class TrendingAIPapersProvider(ContentProvider):
    def get_contents(self) -> List[Content]:
        return get_latest_papers_from_papers_with_code()
