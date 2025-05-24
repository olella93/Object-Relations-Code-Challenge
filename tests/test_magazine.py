from lib.models.magazine import Magazine
from lib.models.author import Author
from lib.db import get_connection

class TestMagazine:
    """Tests for Magazine model (mirrors lib/models/magazine.py)"""
    
    @classmethod
    def setup_class(cls):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.executescript("""
            INSERT INTO magazines (name, category) VALUES ('Test Mag', 'Tech');
            INSERT INTO authors (name) VALUES ('Author A'), ('Author B');
            INSERT INTO articles (title, author_id, magazine_id) VALUES
                ('Article 1', 1, 1),
                ('Article 2', 2, 1);
        """)
        conn.commit()

    def test_contributors(self):
        mag = Magazine.find_by_id(1)
        assert len(mag.contributors()) == 2

    def test_contributing_authors(self):
        mag = Magazine.find_by_id(1)
        
        conn = get_connection()
        conn.execute("INSERT INTO articles (title, author_id, magazine_id) VALUES ('Article 3', 1, 1)")
        assert len(mag.contributing_authors()) == 1