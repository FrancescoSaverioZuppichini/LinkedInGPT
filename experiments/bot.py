import json

from dotenv import load_dotenv

load_dotenv()


from pathlib import Path

from langchain.agents import Tool
from langchain.chat_models import ChatOpenAI
from langchain.memory import ConversationBufferWindowMemory
from rich import print

from db import insert_post
from linkedin.user import User
from logger import logger
from tools.linkedIn import write_linkedin_post
from tools.papers import get_a_trending_paper_for_a_post

user = User()

memory = ConversationBufferWindowMemory(
    memory_key="chat_history", k=5, return_messages=True
)

from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate

prompt = PromptTemplate(
    input_variables=["paper", "bot_name"],
    template=Path("prompts/bot.prompt").read_text(),
)

llm = ChatOpenAI(temperature=0)

paper = get_a_trending_paper_for_a_post(only_from_db=True)

chain = LLMChain(llm=llm, prompt=prompt)

content = chain.run({"paper": json.dumps(paper), "bot_name": "Leonardo"})
print(paper)
print(content)

confirmation = input("Proceed? [y/n]:")
if confirmation == "y":
    print("Writing...")
    write_linkedin_post(user, content, media_url=paper["media"])
