from lib.db.connection import get_connection

class Author:
    def __init__(self, id=None, name=None):
        self.id = id
        self.name = name

    @classmethod
    def all(cls):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM authors")
        rows = cursor.fetchall()
        authors = [cls(row['id'], row['name']) for row in rows]
        conn.close()
        return authors

    def save(self):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO authors (name) VALUES (?) RETURNING id", (self.name,))
        self.id = cursor.fetchone()["id"]
        conn.commit()
        conn.close()

    @staticmethod
    def find_by_id(id):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM authors WHERE id = ?", (id,))
        row = cursor.fetchone()
        conn.close()
        return Author(**row) if row else None

    def articles(self):
        from lib.models.article import Article 
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM articles WHERE author_id = ?", (self.id,))
        rows = cursor.fetchall()
        conn.close()
        return [Article(row['id'], row['title'], row['author_id'], row['magazine_id']) for row in rows]

    def magazines(self):
        from lib.models.magazine import Magazine  
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT DISTINCT m.* FROM magazines m
            JOIN articles a ON m.id = a.magazine_id
            WHERE a.author_id = ?
        """, (self.id,))
        rows = cursor.fetchall()
        conn.close()
        return [Magazine(row['id'], row['name'], row['category']) for row in rows]

    def topic_areas(self):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT DISTINCT m.category FROM magazines m
            JOIN articles a ON m.id = a.magazine_id
            WHERE a.author_id = ?
        """, (self.id,))
        rows = cursor.fetchall()
        conn.close()
        return [row['category'] for row in rows]

    def add_article(self, magazine, title):
        from lib.models.article import Article  
        from lib.models.magazine import Magazine  
        if not isinstance(magazine, Magazine):
            raise TypeError("Expected a Magazine instance")
        article = Article(None, title, self.id, magazine.id)
        article.save()
        return article

    @classmethod
    def author_with_most_articles(cls):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT a.*, COUNT(ar.id) AS article_count
            FROM authors a
            JOIN articles ar ON a.id = ar.author_id
            GROUP BY a.id
            ORDER BY article_count DESC
            LIMIT 1
        """)
        row = cursor.fetchone()
        conn.close()
        if row:
            return cls(row['id'], row['name'])
        return None
    
    @classmethod
    def find_by_name(cls, name):
     conn = get_connection()
     cursor = conn.cursor()
     cursor.execute("SELECT * FROM authors WHERE name = ?", (name,))
     row = cursor.fetchone()
     conn.close()
     return cls(row['id'], row['name']) if row else None

