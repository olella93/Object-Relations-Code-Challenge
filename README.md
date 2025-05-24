# Object Relations Code Challenge: Articles

## Overview
A Python system modeling relationships between Authors, Articles, and Magazines using SQLite with:
- Proper database schema (1-to-many and many-to-many relationships)
- Raw SQL queries in Python classes
- Transaction handling
- Test coverage

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
Class	Key Methods
Author	articles(), magazines(), add_article(), topic_areas()
Magazine	articles(), contributors(), article_titles(), contributing_authors()
Article	Relationship methods to connect authors and magazines

