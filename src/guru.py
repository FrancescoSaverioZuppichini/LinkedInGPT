import random
from typing import Callable, List, Optional

from langchain import LLMChain

from src.actions import Action
from src.content_providers import ContentProvider
from src.storages import Storage
from src.types import Content, GeneratedContent

from src.logger import logger

def random_content_selection_strategy(contents: List[Content]) -> Content:
    return random.choice(contents)


class Guru:
    def __init__(
        self,
        name: str,
        content_provider: ContentProvider,
        storage: Storage,
        action: Action,
        confirmation: Callable[[Callable], bool],
        llm_chain: LLMChain,
        content_selection_strategy: Optional[Callable[[List[Content]], Content]] = None,
    ) -> None:
        self.name = name
        self.content_provider = content_provider
        self.storage = storage
        self.action = action
        self.confirmation = confirmation
        self.llm_chain = llm_chain
        self.content_selection_strategy = (
            random_content_selection_strategy
            if content_selection_strategy is None
            else content_selection_strategy
        )

    def run(self):
        contents = self.content_provider.get_contents()
        list(map(lambda content: self.storage.store(content), contents))
        contents = self.storage.get_all(created=False)
        content = self.content_selection_strategy(contents)
        generated_text = self.llm_chain.run({"content": content.__dict__, "bot_name": self.name})
        logger.info(f"Generated text for content:\n{generated_text}")
        if self.confirmation(self.run):
            logger.info(f"Running action {self.action}")
            # [TODO] here I know in my setup what 'media' will be inside content because I will get it from paperswithcode
            generated_content = GeneratedContent(generated_text, media_url=content.data['media'])
            self.action(generated_content)
            content.created = True
            self.storage.update(content)
            logger.info("Done!")
