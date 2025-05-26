from lib.models.author import Author
from lib.db import get_connection

class TestTransactions:
    """Tests for database transactions (mirrors lib/db/ patterns)"""
    
    def test_rollback_on_error(self):
        initial_count = get_connection().execute("SELECT COUNT(*) FROM authors").fetchone()[0]
        
        # Should fail due to NULL magazine_id
        Author.add_author_with_articles(
            "Fail Author",
            [{"title": "Bad Article", "magazine_id": None}]
        )
        
        new_count = get_connection().execute("SELECT COUNT(*) FROM authors").fetchone()[0]
        assert new_count == initial_count 