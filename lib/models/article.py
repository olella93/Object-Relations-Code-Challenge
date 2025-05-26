from lib.db.connection import get_connection
from lib.models.author import Author
from lib.models.magazine import Magazine

class Article:
    def __init__(self, id, title, author_id, magazine_id):
        self.id = id
        self.title = title
        self.author_id = author_id
        self.magazine_id = magazine_id

    @classmethod
    def all(cls):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM articles")
        rows = cursor.fetchall()
        articles = [cls(row['id'], row['title'], row['author_id'], row['magazine_id']) for row in rows]
        conn.close()
        return articles

    @classmethod
    def find_by_id(cls, id):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM articles WHERE id = ?", (id,))
        row = cursor.fetchone()
        conn.close()
        if row:
            return cls(row['id'], row['title'], row['author_id'], row['magazine_id'])
        return None

    @classmethod
    def find_by_title(cls, title):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM articles WHERE title = ?", (title,))
        rows = cursor.fetchall()
        articles = [cls(row['id'], row['title'], row['author_id'], row['magazine_id']) for row in rows]
        conn.close()
        return articles

    @classmethod
    def find_by_author(cls, author_id):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM articles WHERE author_id = ?", (author_id,))
        rows = cursor.fetchall()
        conn.close()
        return [cls(row['id'], row['title'], row['author_id'], row['magazine_id']) for row in rows]

    @classmethod
    def find_by_magazine(cls, magazine_id):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM articles WHERE magazine_id = ?", (magazine_id,))
        rows = cursor.fetchall()
        conn.close()
        return [cls(row['id'], row['title'], row['author_id'], row['magazine_id']) for row in rows]

    def save(self):
        if not self.title:
            raise ValueError("Article must have a title")
        if not self.author_id or not self.magazine_id:
            raise ValueError("Article must have an author and a magazine")
        conn = get_connection()
        cursor = conn.cursor()
        if self.id is None:
            cursor.execute(
                "INSERT INTO articles (title, author_id, magazine_id) VALUES (?, ?, ?)",
                (self.title, self.author_id, self.magazine_id)
            )
            self.id = cursor.lastrowid
        else:
            cursor.execute(
                "UPDATE articles SET title = ?, author_id = ?, magazine_id = ? WHERE id = ?",
                (self.title, self.author_id, self.magazine_id, self.id)
            )
        conn.commit()
        conn.close()

    def author(self):
        return Author.find_by_id(self.author_id)

    def magazine(self):
        return Magazine.find_by_id(self.magazine_id)

    def __repr__(self):
        return f"<Article {self.id}: {self.title}>"
