from lib.models.article import Article
from lib.db import get_connection

class TestArticle:
    """Tests for Article model (mirrors lib/models/article.py)"""
    
    @classmethod
    def setup_class(cls):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.executescript("""
            INSERT INTO authors (name) VALUES ('Test Author');
            INSERT INTO magazines (name, category) VALUES ('Test Mag', 'Tech');
        """)
        conn.commit()

    def test_save(self):
        article = Article("Test Article", 1, 1)
        article.save()
        assert article.id is not None