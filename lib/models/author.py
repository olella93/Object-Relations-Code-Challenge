from lib.db import get_connection

class Author:
    def __init__(self, name, id=None):
        self.name = name
        self.id = id

    def save(self):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO authors (name) VALUES (?)", (self.name,))
        conn.commit()
        self.id = cursor.lastrowid

    @classmethod
    def find_by_id(cls, id):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM authors WHERE id = ?", (id,))
        row = cursor.fetchone()
        return cls(row['name'], row['id']) if row else None

    def articles(self):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM articles WHERE author_id = ?", (self.id,))
        return cursor.fetchall()

    def magazines(self):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT DISTINCT magazines.* FROM magazines
            JOIN articles ON magazines.id = articles.magazine_id
            WHERE articles.author_id = ?
        """, (self.id,))
        return cursor.fetchall()

    def add_article(self, magazine, title):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO articles (title, author_id, magazine_id) VALUES (?, ?, ?)",
            (title, self.id, magazine.id)
        )
        conn.commit()

    def topic_areas(self):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT DISTINCT category FROM magazines
            JOIN articles ON magazines.id = articles.magazine_id
            WHERE articles.author_id = ?
        """, (self.id,))
        return [row['category'] for row in cursor.fetchall()]
    
    
def add_author_with_articles(author_name, articles_data):
    conn = get_connection()
    try:
        conn.execute("BEGIN TRANSACTION")
        cursor = conn.cursor()
        
        # Insert author
        cursor.execute(
            "INSERT INTO authors (name) VALUES (?) RETURNING id",
            (author_name,)
        )
        author_id = cursor.fetchone()[0]
        
        # Insert articles
        for article in articles_data:
            cursor.execute(
                "INSERT INTO articles (title, author_id, magazine_id) VALUES (?, ?, ?)",
                (article['title'], author_id, article['magazine_id'])
            )
        
        conn.commit()
        return True
    except Exception as e:
        conn.rollback()
        print(f"Transaction failed: {e}")
        return False
    finally:
        conn.close()