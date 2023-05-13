import json
import sqlite3
from typing import Dict, List, Optional, TypedDict

from src.types import Content

from .base import Storage


class SQLiteStorage(Storage):
    def __init__(self, name: str = "content.db"):
        self.conn = sqlite3.connect(name)
        self._init_table()

    def _init_table(self):
        cursor = self.conn.cursor()
        cursor.execute(
            """
        CREATE TABLE IF NOT EXISTS content (
            uid TEXT PRIMARY KEY,
            data TEXT,
            created INTEGER
        )
        """
        )
        self.conn.commit()

    def store(self, content: Content):
        cursor = self.conn.cursor()
        cursor.execute(
            """
        INSERT OR IGNORE INTO content (uid, data, created) VALUES (?, ?, ?)
        """,
            (content.uid, json.dumps(content.data), int(content.created)),
        )
        self.conn.commit()

    def update(self, updated_content: Content):
        cursor = self.conn.cursor()
        cursor.execute(
            """
        UPDATE content
        SET data = ?, created = ?
        WHERE uid = ?
        """,
            (
                json.dumps(updated_content.data),
                int(updated_content.created),
                updated_content.uid,
            ),
        )
        self.conn.commit()

    def get_all(self, created: Optional[bool] = None) -> List[Content]:
        cursor = self.conn.cursor()

        if created is None:
            cursor.execute("SELECT uid, data, created FROM content")
        else:
            cursor.execute(
                "SELECT uid, data, created FROM content WHERE created=?",
                (int(created),),
            )

        results = cursor.fetchall()

        contents = [
            Content(uid=row[0], data=json.loads(row[1]), created=bool(row[2]))
            for row in results
        ]

        return contents

    def close(self):
        self.conn.close
