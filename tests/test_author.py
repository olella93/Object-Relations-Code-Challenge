from lib.models.author import Author
from lib.models.magazine import Magazine
from lib.models.article import Article
from lib.db import get_connection

def test_author_save():
    author = Author("Jane Doe")
    author.save()
    assert author.id is not None

def test_author_articles():
    author = Author("John Smith")
    author.save()
    magazine = Magazine("Tech Today", "Technology")
    magazine.save()
    
    Article("Python Tips", author.id, magazine.id).save()
    articles = author.articles()
    assert len(articles) == 1
    assert articles[0]['title'] == "Python Tips"