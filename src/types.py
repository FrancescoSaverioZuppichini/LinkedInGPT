from dataclasses import dataclass
from typing import Any, Dict, Optional


@dataclass
class Content:
    uid: str
    data: Dict[str, Any]
    created: Optional[bool] = False


@dataclass
class GeneratedContent:
    text: str
    medial_url: Optional[str] = None
