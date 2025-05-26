from lib.models.author import Author
from lib.models.magazine import Magazine
from lib.db import get_connection

class TestRelationships:
    """Tests cross-model relationships (mirrors domain model)"""
    
    @classmethod
    def setup_class(cls):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.executescript("""
            INSERT INTO authors (name) VALUES ('Author X');
            INSERT INTO magazines (name, category) VALUES ('Mag Y', 'Science');
            INSERT INTO articles (title, author_id, magazine_id) VALUES
                ('Rel Test 1', 1, 1),
                ('Rel Test 2', 1, 1);
        """)
        conn.commit()

    def test_author_magazines(self):
        author = Author.find_by_id(1)
        assert len(author.magazines()) == 1
        assert author.magazines()[0]['name'] == "Mag Y"

    def test_magazine_authors(self):
        mag = Magazine.find_by_id(1)
        assert len(mag.contributors()) == 1