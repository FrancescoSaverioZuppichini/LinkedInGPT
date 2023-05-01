import os
from dotenv import load_dotenv

load_dotenv()

from langchain.agents import Tool
from langchain.experimental import AutoGPT
from langchain.chat_models import ChatOpenAI
from langchain.memory import ConversationBufferWindowMemory
import requests
from bs4 import BeautifulSoup
import json
from rich import print
from langchain.vectorstores import FAISS
from langchain.docstore import InMemoryDocstore
from langchain.embeddings import OpenAIEmbeddings
import faiss
from pathlib import Path
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

    return json.dumps(result)


def write_linkedin_post(content):
    user.create_post(
        content
        + "\n#opensource #llms #datascience #machinelearning #programming #ai #ds #python #deeplearning #nlp"
    )
    return "Post created! Good job!"


def get_latest_papers(*args, **kwargs):
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
            results.append(paper_dict)
        else:
            print("No div element with the specified class was found")
    else:
        print(f"Failed to fetch the webpage. Status code: {response.status_code}")

    return json.dumps(results)


tools = [
    Tool(
        name="get_latest_papers",
        func=get_latest_papers,
        description="Use this to find new and trending AI papers, it returns a JSON.",
    ),
    Tool(
        name="get_paper_info",
        func=get_paper_info,
        description="Use this tool to get the abstract and the arxiv link from a `uid`. It will return a JSON. You need to pass the `uid`",
    ),
    Tool(
        name="write LinkedIn post",
        func=write_linkedin_post,
        description="Use it to write a LinkedIn post, input should be the post's content.",
    ),
]

memory = ConversationBufferWindowMemory(
    memory_key="chat_history", k=3, return_messages=True
)

# Define your embedding model
embeddings_model = OpenAIEmbeddings()
# Initialize the vectorstore as empty

embedding_size = 1536
index = faiss.IndexFlatL2(embedding_size)
vectorstore = FAISS(embeddings_model.embed_query, index, InMemoryDocstore({}), {})

agent = AutoGPT.from_llm_and_tools(
    ai_name="Jacob",
    ai_role="Assistant",
    tools=tools,
    llm=ChatOpenAI(temperature=0),
    memory=vectorstore.as_retriever(),
)
# Set verbose to be true
# agent.chain.verbose = True

agent.run([Path("goal.prompt").read_text()])
