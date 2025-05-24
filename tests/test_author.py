from lib.models.author import Author
from lib.models.magazine import Magazine
from lib.db import get_connection

class TestAuthor:
    """Tests for Author model (mirrors lib/models/author.py)"""
    
    @classmethod
    def setup_class(cls):
        """Seed test data"""
        conn = get_connection()
        cursor = conn.cursor()
        cursor.executescript("""
            DELETE FROM articles;
            DELETE FROM authors;
            INSERT INTO authors (name) VALUES ('Test Author');
        """)
        conn.commit()

    def test_save(self):
        author = Author("Jane Doe")
        author.save()
        assert author.id is not None

    def test_add_article(self):
        author = Author.find_by_id(1)
        magazine = Magazine("Tech Weekly", "Technology")
        magazine.save()
        
        author.add_article(magazine, "New Article")
        assert len(author.articles()) == 1