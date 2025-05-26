from lib.db.connection import get_connection

def seed_data():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.executescript("""
        DELETE FROM articles;
        DELETE FROM authors;
        DELETE FROM magazines;

        INSERT INTO authors (name) VALUES ('Alice'), ('Bob'), ('Clara');
        INSERT INTO magazines (name, category) VALUES ('Tech Weekly', 'Technology'), ('Health First', 'Health');
        INSERT INTO articles (title, author_id, magazine_id) VALUES
            ('AI in 2025', 1, 1),
            ('The Future of Medicine', 2, 2),
            ('Wearables and Health', 1, 2),
            ('Quantum Leap', 1, 1),
            ('Nutrition Myths', 3, 2);
    """)
    conn.commit()
    conn.close()