from lib.db.connection import get_connection
from lib.models.author import Author
from lib.models.article import Article

class Magazine:
    def __init__(self, id, name, category):
        self.id = id
        self.name = name
        self.category = category

    @classmethod
    def all(cls):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM magazines")
        rows = cursor.fetchall()
        magazines = [cls(row['id'], row['name'], row['category']) for row in rows]
        conn.close()
        return magazines

    @classmethod
    def find_by_id(cls, id):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM magazines WHERE id = ?", (id,))
        row = cursor.fetchone()
        conn.close()
        if row:
            return cls(row['id'], row['name'], row['category'])
        return None

    @classmethod
    def find_by_name(cls, name):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM magazines WHERE name = ?", (name,))
        row = cursor.fetchone()
        conn.close()
        if row:
            return cls(row['id'], row['name'], row['category'])
        return None

    @classmethod
    def find_by_category(cls, category):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM magazines WHERE category = ?", (category,))
        rows = cursor.fetchall()
        magazines = [cls(row['id'], row['name'], row['category']) for row in rows]
        conn.close()
        return magazines

    def save(self):
        if not self.name or not self.category:
            raise ValueError("Magazine must have a name and category")
        conn = get_connection()
        cursor = conn.cursor()
        if self.id is None:
            cursor.execute(
                "INSERT INTO magazines (name, category) VALUES (?, ?)",
                (self.name, self.category)
            )
            self.id = cursor.lastrowid
        else:
            cursor.execute(
                "UPDATE magazines SET name = ?, category = ? WHERE id = ?",
                (self.name, self.category, self.id)
            )
        conn.commit()
        conn.close()

    def articles(self):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM articles WHERE magazine_id = ?", (self.id,))
        rows = cursor.fetchall()
        conn.close()
        return [Article(row['id'], row['title'], row['author_id'], row['magazine_id']) for row in rows]

    def contributors(self):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT DISTINCT a.* FROM authors a
            JOIN articles ar ON a.id = ar.author_id
            WHERE ar.magazine_id = ?
        """, (self.id,))
        rows = cursor.fetchall()
        conn.close()
        return [Author(row['id'], row['name']) for row in rows]

    def article_titles(self):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT title FROM articles WHERE magazine_id = ?", (self.id,))
        rows = cursor.fetchall()
        conn.close()
        return [row['title'] for row in rows]

    def contributing_authors(self):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT a.id, a.name, COUNT(ar.id) as article_count
            FROM authors a
            JOIN articles ar ON a.id = ar.author_id
            WHERE ar.magazine_id = ?
            GROUP BY a.id
            HAVING article_count > 2
        """, (self.id,))
        rows = cursor.fetchall()
        conn.close()
        return [Author(row['id'], row['name']) for row in rows]

    @classmethod
    def top_publisher(cls):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT m.*, COUNT(ar.id) as article_count
            FROM magazines m
            LEFT JOIN articles ar ON m.id = ar.magazine_id
            GROUP BY m.id
            ORDER BY article_count DESC
            LIMIT 1
        """)
        row = cursor.fetchone()
        conn.close()
        if row:
            return cls(row['id'], row['name'], row['category'])
        return None

    def __repr__(self):
        return f"<Magazine {self.id}: {self.name} ({self.category})>"

    @classmethod
    def authors_for_magazine(cls, magazine_id):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT DISTINCT a.* FROM authors a
            JOIN articles ar ON a.id = ar.author_id
            WHERE ar.magazine_id = ?
        """, (magazine_id,))
        rows = cursor.fetchall()
        conn.close()
        return [Author(row['id'], row['name']) for row in rows]

    @classmethod
    def magazines_with_two_or_more_authors(cls):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT m.*, COUNT(DISTINCT ar.author_id) AS author_count
            FROM magazines m
            JOIN articles ar ON m.id = ar.magazine_id
            GROUP BY m.id
            HAVING author_count >= 2
        """)
        rows = cursor.fetchall()
        conn.close()
        return [cls(row['id'], row['name'], row['category']) for row in rows]

    @classmethod
    def article_counts(cls):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT m.name, COUNT(ar.id) AS article_count
            FROM magazines m
            LEFT JOIN articles ar ON m.id = ar.magazine_id
            GROUP BY m.id
        """)
        rows = cursor.fetchall()
        conn.close()
        return {row['name']: row['article_count'] for row in rows}

    @classmethod
    def magazines_with_multiple_authors(cls):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT m.*, COUNT(DISTINCT ar.author_id) AS author_count
            FROM magazines m
            JOIN articles ar ON m.id = ar.magazine_id
            GROUP BY m.id
            HAVING author_count > 1
        """)
        rows = cursor.fetchall()
        conn.close()
        return [cls(row['id'], row['name'], row['category']) for row in rows]