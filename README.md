# Object Relations Code Challenge: Articles

## Overview
A Python system modeling relationships between Authors, Articles, and Magazines using SQLite with:
- Proper database schema (1-to-many and many-to-many relationships)
- Raw SQL queries in Python classes
- Transaction handling
- Test coverage

### Project Structure

.
├── lib/

│   ├── models/

│   │   ├── author.py

│   │   ├── magazine.py

│   │   └── article.py

│   └── db/

│       ├── connection.py

│       └── seed.py

├── tests/

│   ├── test_article.py

│   ├── test_author.py

│   └── test_magazine.py

├── .venv/

├── README.md

└── requirements.txt


## Setup
1. **Install dependencies**:
   ```bash
   pip install pytest sqlite3

### Initialize database:

python scripts/setup_db.py

### Run tests:
pytest

### Domain Model

![Domain Model](https://i.imgur.com/SOSGjF6.png)


### Key Features
Class	 Key Methods

Author	articles(), magazines(), add_article(), topic_areas()

Magazine	articles(), contributors(), article_titles(), contributing_authors()

Article	Relationship methods to connect authors and magazines

### Database Schema
See lib/db/schema.sql for:

- Table definitions

- Foreign key constraints

- Performance indexes

### Testing
Run all tests:

pytest tests/

### 🧠 Key Models and Methods
Author

- Author.all()

- Author.find_by_name(name)

- author.articles()

- author.magazines()

- author.add_article(title, magazine)

- author.topic_areas()

## Magazine

- Magazine.all()

- Magazine.find_by_name(name)

- magazine.articles()

- magazine.contributors()

- magazine.article_titles()

- magazine.contributing_authors()

## Article

- Article.all()

- Article.find_by_title(title)

- Article.find_by_author(author)

- Article.find_by_magazine(magazine)

### 📌 Requirements

- Python 3.8+

- SQLite (via sqlite3 built-in module)

- pytest for running tests

### 🙌 Credits

Developed as part of the Moringa Phase 3 Software Engineering curriculum challenge.

### 📝 License

MIT License (or your preferred license)
