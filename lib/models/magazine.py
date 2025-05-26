from lib.db.connection import get_connection

class Magazine:
    def __init__(self, id=None, name=None, category=None):
        self.id = id
        self.name = name
        self.category = category

    def save(self):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO magazines (name, category) VALUES (?, ?) RETURNING id", (self.name, self.category))
        self.id = cursor.fetchone()["id"]
        conn.commit()
        conn.close()

    def articles(self):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM articles WHERE magazine_id = ?", (self.id,))
        return cursor.fetchall()

    def contributors(self):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT DISTINCT a.* FROM authors a
            JOIN articles art ON a.id = art.author_id
            WHERE art.magazine_id = ?
        """, (self.id,))
        return cursor.fetchall()

    def article_titles(self):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT title FROM articles WHERE magazine_id = ?", (self.id,))
        return [row["title"] for row in cursor.fetchall()]

    def contributing_authors(self):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT a.*, COUNT(*) as article_count FROM authors a
            JOIN articles art ON a.id = art.author_id
            WHERE art.magazine_id = ?
            GROUP BY a.id
            HAVING COUNT(*) > 2
        """, (self.id,))
        return cursor.fetchall()

    @staticmethod
    def top_publisher():
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT m.*, COUNT(a.id) as count FROM magazines m
            JOIN articles a ON m.id = a.magazine_id
            GROUP BY m.id
            ORDER BY count DESC
            LIMIT 1
        """)
        return cursor.fetchone()