import sys

# lazy to make a package
sys.path.append(".")
from dotenv import load_dotenv

load_dotenv()

from pathlib import Path

from langchain.chains import LLMChain
from langchain.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate

from src.actions.linkedIn import PostOnLinkedInAction
from src.confirmations.input_confirmation import input_confirmation
from src.content_providers import TrendingAIPapersProvider
from src.guru import Guru
from src.storages import SQLiteStorage

prompt = PromptTemplate(
    input_variables=["content", "bot_name"],
    template=Path("prompts/guru.prompt").read_text(),
)

llm = ChatOpenAI(temperature=0)

chain = LLMChain(llm=llm, prompt=prompt)

guru = Guru(
    name="Leonardo",
    content_provider=TrendingAIPapersProvider(),
    storage=SQLiteStorage(),
    action=PostOnLinkedInAction(),
    confirmation=input_confirmation,
    llm_chain=chain
)

guru.run()