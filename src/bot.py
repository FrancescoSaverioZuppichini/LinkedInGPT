import json

from dotenv import load_dotenv

load_dotenv()


from pathlib import Path
from langchain.agents import Tool
from langchain.chat_models import ChatOpenAI
from langchain.memory import ConversationBufferWindowMemory

from logger import logger

from db import insert_post
from tools.papers import get_a_trending_paper_for_a_post
from tools.linkedIn import write_linkedin_post
from linkedin.user import User

user = User()

memory = ConversationBufferWindowMemory(
    memory_key="chat_history", k=5, return_messages=True
)

from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain

prompt = PromptTemplate(
    input_variables=["paper"],
    template=Path("prompts/bot.prompt").read_text(),
)

llm = ChatOpenAI(temperature=0)

paper = get_a_trending_paper_for_a_post()

chain = LLMChain(llm=llm, prompt=prompt)

content = chain.run(json.dumps(paper))
print(paper)
print(content)