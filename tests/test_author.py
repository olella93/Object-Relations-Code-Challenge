import pytest
from lib.db.seed import seed_data
from lib.models.author import Author
from lib.models.magazine import Magazine

@pytest.fixture(scope="module", autouse=True)
def setup_db():
    seed_data()
    yield

def test_author_all():
    authors = Author.all()
    assert len(authors) > 0

def test_find_by_id_and_name():
    author = Author.find_by_id(1)
    assert author is not None
    author2 = Author.find_by_name(author.name)
    assert author2.id == author.id

def test_author_articles():
    author = Author.all()[0]
    articles = author.articles()
    assert isinstance(articles, list)
    for article in articles:
        assert article.author_id == author.id

def test_author_magazines():
    author = Author.all()[0]
    magazines = author.magazines()
    assert isinstance(magazines, list)
    for mag in magazines:
        assert hasattr(mag, "name")
        assert hasattr(mag, "category")

def test_add_article():
    author = Author.all()[0]
    magazines = Magazine.all()
    magazine = magazines[0]
    title = "Pytest Article"

    article = author.add_article(magazine, title)
    assert article.title == title
    assert article.author_id == author.id
    assert article.magazine_id == magazine.id

def test_topic_areas():
    author = Author.all()[0]
    topics = author.topic_areas()
    assert isinstance(topics, list)
    assert all(isinstance(topic, str) for topic in topics)
