from lib.db.connection import get_connection
from lib.models.author import Author
from lib.models.article import Article

def add_author_with_articles(author_name, articles_info):
    """
    articles_info: list of dicts like [{title: str, magazine: Magazine instance}, ...]
    """
    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO authors (name) VALUES (?)", (author_name,))
        author_id = cursor.lastrowid

        for article_data in articles_info:
            title = article_data['title']
            magazine = article_data['magazine']
            cursor.execute(
                "INSERT INTO articles (title, author_id, magazine_id) VALUES (?, ?, ?)",
                (title, author_id, magazine.id)
            )
        conn.commit()
        return Author.find_by_id(author_id)
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        conn.close()
