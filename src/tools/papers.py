
from typing import List, Dict

import requests
from bs4 import BeautifulSoup
import json
from random import choice
from db import Paper
from db import insert_paper, get_all_papers_without_a_post, init_db
from logger import logger

def get_paper_info_from_papers_with_code(uid: str, *args, **kwargs) -> Dict:
    """
    Fetching the paper little summary page on papers with code, e.g. 
    https://paperswithcode.com/paper/track-anything-segment-anything-meets-videos

    This function returns a dictionary with `abtract` and `arxiv_link`.
    """
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
        logger.warning(
            f"Failed to fetch https://paperswithcode.com{uid}. Status code: {response.status_code}"
        )

    return result

def get_latest_papers_from_papers_with_code(*args, **kwargs) -> List[Paper]:
    logger.info("Getting papers from https://paperswithcode.com/")
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
            results.append({**paper_dict, **get_paper_info_from_papers_with_code(paper_dict["uid"])})
        else:
            logger.warning("Was not able to scrape the html for one row.")
    else:
        logger.warning(f"Failed to fetch the webpage. Status code: {response.status_code}.")

    return results


def get_a_trending_paper_for_a_post(only_from_db: bool = False) -> Paper:
    conn = init_db()
    if not only_from_db:
        papers = get_latest_papers_from_papers_with_code(conn)
        logger.debug(json.dumps(papers, indent=4))
        [insert_paper(conn, paper) for paper in papers]
    papers_without_a_post = get_all_papers_without_a_post(conn)
    return choice(papers_without_a_post)