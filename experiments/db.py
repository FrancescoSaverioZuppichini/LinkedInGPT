import sqlite3
from typing import List, TypedDict

"""
Basically some poor man CRUD functions to store papers and post inside a sqlite db.
"""


class Paper(TypedDict):
    uid: str
    title: str
    subtitle: str
    abstract: str
    media: str
    tags: List[str]
    stars: int
    github_link: str
    arxiv_link: str


class Post(TypedDict):
    paper_uid: str
    text: str
    media: str


def create_connection() -> sqlite3.Connection:
    return sqlite3.connect("agent.db")


def row_to_dict(cursor, row):
    return {col[0]: row[idx] for idx, col in enumerate(cursor.description)}


def create_table_papers(conn: sqlite3.Connection):
    cur = conn.cursor()
    cur.execute(
        """CREATE TABLE IF NOT EXISTS papers (
                                    uid TEXT PRIMARY KEY,
                                    title TEXT NOT NULL,
                                    subtitle TEXT,
                                    abstract TEXT,
                                    media TEXT,
                                    tags TEXT,
                                    stars INTEGER,
                                    github_link TEXT,
                                    arxiv_link TEXT
                                );"""
    )


def delete_paper(conn: sqlite3.Connection, uid: str):
    sql = "DELETE FROM papers WHERE uid=?"
    cur = conn.cursor()
    cur.execute(sql, (uid,))
    conn.commit()


def insert_paper(conn: sqlite3.Connection, paper: Paper):
    sql = """INSERT OR IGNORE INTO papers(uid, title, subtitle, abstract, media, tags, stars, github_link, arxiv_link)
             VALUES(:uid, :title, :subtitle, :abstract, :media, :tags, :stars, :github_link, :arxiv_link)"""
    cur = conn.cursor()
    cur.execute(
        sql,
        {
            "uid": paper["uid"],
            "title": paper["title"],
            "subtitle": paper["subtitle"],
            "abstract": paper["abstract"],
            "media": paper["media"],
            "tags": ",".join(paper["tags"]),
            "stars": paper["stars"],
            "github_link": paper["github_link"],
            "arxiv_link": paper["arxiv_link"],
        },
    )
    conn.commit()
    return cur.lastrowid


def get_all_papers(conn: sqlite3.Connection) -> List[Paper]:
    cur = conn.cursor()
    cur.execute("SELECT * FROM papers")
    rows = cur.fetchall()
    return [row_to_dict(cur, row) for row in rows]


def get_paper_by_uid(conn: sqlite3.Connection, uid: str) -> Paper:
    cur = conn.cursor()
    cur.execute("SELECT * FROM papers WHERE uid=?", (uid,))
    row = cur.fetchone()
    if row:
        return row_to_dict(cur, row)
    return None


def create_post_table(conn: sqlite3.Connection):
    cursor = conn.cursor()
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS posts (
            paper_uid TEXT PRIMARY KEY,
            text TEXT,
            media TEXT
        )
    """
    )
    conn.commit()


def insert_post(conn: sqlite3.Connection, post: Post):
    cursor = conn.cursor()
    cursor.execute(
        """
        INSERT INTO posts (paper_uid, text, media) VALUES (?, ?, ?)
    """,
        (post["paper_uid"], post["text"], post["media"]),
    )
    conn.commit()


def get_all_posts(conn: sqlite3.Connection) -> List[Post]:
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM posts")
    rows = cursor.fetchall()
    return [row_to_dict(cursor, row) for row in rows]


def get_all_papers_without_a_post(conn: sqlite3.Connection) -> List[Paper]:
    cursor = conn.cursor()
    cursor.execute(
        """
        SELECT papers.* FROM papers
        LEFT JOIN posts ON papers.uid = posts.paper_uid
        WHERE posts.paper_uid IS NULL
    """
    )
    rows = cursor.fetchall()
    return [row_to_dict(cursor, row) for row in rows]


def init_db() -> sqlite3.Connection:
    conn = create_connection()
    create_table_papers(conn)
    create_post_table(conn)
    return conn


if __name__ == "__main__":
    conn = create_connection()
    create_table_papers(conn)
    create_post_table(conn)

    insert_paper(
        conn,
        Paper(
            uid="foo1",
            title="FOO1",
            subtitle="baa",
            abstract="asddsa",
            media="/media.png",
            tags=["foo"],
            stars=10,
            github_link="github/foo",
            arxiv_link="arxiv/foo",
        ),
    )
    insert_paper(
        conn,
        Paper(
            uid="foo2",
            title="FOO2",
            subtitle="baa",
            abstract="asddsa",
            media="/media.png",
            tags=["foo"],
            stars=10,
            github_link="github/foo",
            arxiv_link="arxiv/foo",
        ),
    )
    papers = get_all_papers(conn)

    post = Post(paper_uid=papers[0]["uid"], text="a post", media="example.com")
    insert_post(conn, post)
    print(get_all_posts(conn))
    print(get_all_papers_without_a_post(conn))
