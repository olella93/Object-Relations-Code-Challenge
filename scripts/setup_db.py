"""
Initialize the test database with schema and seed data
(Mirrors instructions in 'Database Setup' section)
"""

import sys
import os

# Dynamically add the project root directory to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from lib.db.connection import get_connection

def setup_database():
    conn = get_connection()
    cursor = conn.cursor()
    
    # Drop existing tables (clean slate)
    cursor.executescript("""
        DROP TABLE IF EXISTS articles;
        DROP TABLE IF EXISTS authors;
        DROP TABLE IF EXISTS magazines;
    """)
    
    # Create tables (from schema.sql)
    cursor.executescript("""
        CREATE TABLE authors (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL
        );
        
        CREATE TABLE magazines (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            category TEXT NOT NULL
        );
        
        CREATE TABLE articles (
            id INTEGER PRIMARY KEY,
            title TEXT NOT NULL,
            author_id INTEGER,
            magazine_id INTEGER,
            FOREIGN KEY (author_id) REFERENCES authors(id),
            FOREIGN KEY (magazine_id) REFERENCES magazines(id)
        );
        
        -- Add indexes
        CREATE INDEX idx_author ON articles(author_id);
        CREATE INDEX idx_magazine ON articles(magazine_id);
    """)
    
    # Seed test data
    cursor.executescript("""
        INSERT INTO authors (name) VALUES 
            ('J.K. Rowling'),
            ('Stephen King');
            
        INSERT INTO magazines (name, category) VALUES
            ('Wizard Weekly', 'Fantasy'),
            ('Horror Today', 'Horror');
            
        INSERT INTO articles (title, author_id, magazine_id) VALUES
            ('Harry Potter Draft', 1, 1),
            ('IT Prequel', 2, 2);
    """)
    
    conn.commit()
    print("✅ Database initialized with schema and test data")

if __name__ == "__main__":
    setup_database()