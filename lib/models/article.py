from lib.db import get_connection

class Article:
    def __init__(self, title, author_id, magazine_id, id=None):
        self.title = title
        self.author_id = author_id
        self.magazine_id = magazine_id
        self.id = id

    def save(self):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO articles (title, author_id, magazine_id) VALUES (?, ?, ?)",
            (self.title, self.author_id, self.magazine_id)
        )
        conn.commit()
        self.id = cursor.lastrowid