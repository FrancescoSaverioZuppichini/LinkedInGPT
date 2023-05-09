import os

from dotenv import load_dotenv

load_dotenv()
import json
import random
from functools import partial
from pathlib import Path
from typing import List

import requests
from bs4 import BeautifulSoup
from langchain.agents import Tool, initialize_agent, load_tools
from langchain.chat_models import ChatOpenAI
from langchain.experimental import AutoGPT
from langchain.memory import (ConversationBufferMemory,
                              ConversationBufferWindowMemory)
from langchain.tools.file_management.read import ReadFileTool
from langchain.tools.file_management.write import WriteFileTool
from langchain.utilities import (ArxivAPIWrapper, GoogleSearchAPIWrapper,
                                 TextRequestsWrapper)
from rich import print

from db import Paper
from linkedin.user import User

user = User()


def get_paper_info(uid: str, *args, **kwargs):
    response = requests.get(f"https://paperswithcode.com{uid}")
    result = {}
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, "html.parser")
        paper_abstract_div = soup.select_one(".paper-abstract")
        # Extract the abstract
        abstract = paper_abstract_div.find("p").text.strip()
        # Extract the arXiv URL
        arxiv_url = paper_abstract_div.find("a", class_="badge badge-light")["href"]

        result = {"abstract": abstract, "arxiv_link": arxiv_url}

    else:
        print(
            f"Failed to fetch https://paperswithcode.com{uid}. Status code: {response.status_code}"
        )

    return result


def write_linkedin_post(content: str, media_url: str):
    file_path = f"media.{Path(media_url).suffix}"
    with open(file_path, "wb") as f:
        f.write(requests.get(media_url).content)
    user.create_post(
        content
        + "\n#opensource #llms #datascience #machinelearning #programming #ai #ds #python #deeplearning #nlp",
        [(file_path, "media")],
    )
    return "Post created! Good job!"


def get_latest_papers(*args, **kwargs) -> List[Paper]:
    response = requests.get("https://paperswithcode.com/")
    results = []
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, "html.parser")
        for row in soup.select(
            ".infinite-container .row.infinite-item.item.paper-card"
        ):
            paper_dict = {
                "title": row.select_one("h1 a").get_text(strip=True),
                "subtitle": row.select_one(".item-strip-abstract").get_text(strip=True),
                "media": row.select_one(".item-image")["style"]
                .split("('")[1]
                .split("')")[0],
                "tags": [
                    a.get_text(strip=True) for a in row.select(".badge-primary a")
                ],
                "stars": int(
                    row.select_one(".entity-stars .badge")
                    .get_text(strip=True)
                    .split(" ")[0]
                    .replace(",", "")
                ),
                "github_link": row.select_one(".item-github-link a")["href"],
                "uid": row.select_one("h1 a")["href"],
            }
            paper_dict = paper_dict
            results.append({**paper_dict, **get_paper_info(paper_dict["uid"])})
        else:
            print("No div element with the specified class was found")
    else:
        print(f"Failed to fetch the webpage. Status code: {response.status_code}")

    return results


def get_a_trending_paper(*args, **kwargs) -> Paper:
    papers = get_latest_papers()
    print(papers)
    paper = random.choice(papers)
    return paper


# write_linkedin_post(
#     "foo",
#     "https://production-media.paperswithcode.com/thumbnails/papergithubrepo/3ef6f4ee-4b0b-4654-8bcb-9f0f1299261f.jpg",
# )

# print(get_a_trending_paper())

tools = [
    Tool(
        name="get_a_trending_paper",
        func=get_a_trending_paper,
        description="Use this to find a new and trending AI paper, it returns a JSON with information about a paper.",
    ),
    #     # Tool(
    #     #     name="get_paper_info",
    #     #     func=get_paper_info,
    #     #     description="Use this tool to get the abstract and the arxiv link from a `uid`. It will return a JSON. You need to pass the `uid`",
    #     # ),
    # Tool(
    #     name="write LinkedIn post",
    #     func=write_linkedin_post,
    #     description="Use it to write a LinkedIn post, input is the post's content and an image url.",
    # ),
]

memory = ConversationBufferWindowMemory(
    memory_key="chat_history", k=10, return_messages=True
)

from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain

prompt = PromptTemplate(
    input_variables=["paper"],
    template=Path("goal_agent.prompt").read_text(),
)


llm = ChatOpenAI(temperature=0)

paper = get_a_trending_paper()

chain = LLMChain(llm=llm, prompt=prompt)

content = chain.run(json.dumps(paper))
print(paper)
print(content)
# write_linkedin_post(content, paper['media'])

# conversational_agent = initialize_agent(
#     agent="chat-conversational-react-description",
#     tools=tools,
#     llm=ChatOpenAI(temperature=0),
#     verbose=True,
#     max_iterations=10,
#     early_stopping_method="generate",
#     memory=memory,
# )


# print(conversational_agent.run(Path("goal_agent.prompt").read_text()))
# {
#     'title': 'Harnessing the Power of LLMs in Practice: A Survey on ChatGPT and Beyond',
#     'subtitle': 'This paper presents a comprehensive and practical guide for practitioners and end-users working with Large Language Models (LLMs) in their downstream natural language processing (NLP) tasks.',
#     'media': 'https://production-media.paperswithcode.com/thumbnails/papergithubrepo/16d0f450-e5e7-4471-9a8b-42727da19551.gif',
#     'tags': [],
#     'stars': 2156,
#     'github_link': 'https://github.com/mooler0410/llmspracticalguide',
#     'uid': '/paper/harnessing-the-power-of-llms-in-practice-a',
#     'abstract': 'This paper presents a comprehensive and practical guide for practitioners and end-users working with Large Language Models (LLMs) in their downstream natural language processing (NLP) tasks. We provide discussions and insights into the usage of LLMs from the perspectives of models, data, and downstream tasks. 
# Firstly, we offer an introduction and brief summary of current GPT- and BERT-style LLMs. Then, we discuss the influence of pre-training data, training data, and test data. Most importantly, we provide a detailed discussion about the use and non-use cases of large language models for various natural language processing tasks, 
# such as knowledge-intensive tasks, traditional natural language understanding tasks, natural language generation tasks, emergent abilities, and considerations for specific tasks.We present various use cases and non-use cases to illustrate the practical applications and limitations of LLMs in real-world scenarios. We also try to 
# understand the importance of data and the specific challenges associated with each NLP task. Furthermore, we explore the impact of spurious biases on LLMs and delve into other essential considerations, such as efficiency, cost, and latency, to ensure a comprehensive understanding of deploying LLMs in practice. This comprehensive
# guide aims to provide researchers and practitioners with valuable insights and best practices for working with LLMs, thereby enabling the successful implementation of these models in a wide range of NLP tasks. A curated list of practical guide resources of LLMs, regularly updated, can be found at 
# \\url{https://github.com/Mooler0410/LLMsPracticalGuide}.',
#     'arxiv_link': 'https://arxiv.org/pdf/2304.13712v2.pdf'
# }
Unlock the Power of Large Language Models in NLP Tasks 🤖📝


This paper provides a practical guide for practitioners and end-users working with Large Language Models (LLMs) in their downstream natural language processing (NLP) tasks. Key takeaways include: 

▪️ Understanding the influence of pre-training data, training data, and test data on LLMs 
▪️ Detailed discussion of use and non-use cases of LLMs for various NLP tasks 
▪️ Importance of data and specific challenges associated with each NLP task 
▪️ Impact of spurious biases on LLMs and other essential considerations 

🔗 GitHub: https://github.com/mooler0410/llmspracticalguide
🔗 Arvix: https://arxiv.org/pdf/2304.13712v2.pdf