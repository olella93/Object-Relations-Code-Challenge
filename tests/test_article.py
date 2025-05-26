import pytest
from lib.db.seed import seed_data
from lib.models.article import Article
from lib.models.author import Author
from lib.models.magazine import Magazine

@pytest.fixture(scope="module", autouse=True)
def setup_db():
    seed_data()
    yield

def test_article_all():
    articles = Article.all()
    assert len(articles) > 0

def test_find_by_id_and_title():
    article = Article.all()[0]
    found = Article.find_by_id(article.id)
    assert found.id == article.id

    found_title = Article.find_by_title(article.title)
    assert any(a.title == article.title for a in found_title)

def test_find_by_author():
    author = Author.all()[0]
    articles = Article.find_by_author(author.id)
    assert isinstance(articles, list)
    for article in articles:
        assert article.author_id == author.id

def test_find_by_magazine():
    mag = Magazine.all()[0]
    articles = Article.find_by_magazine(mag.id)
    assert isinstance(articles, list)
    for article in articles:
        assert article.magazine_id == mag.id

def test_article_validation():
    with pytest.raises(ValueError):
        Article(None, None, 1, 1)  

def test_save_article():
    author = Author.all()[0]
    magazine = Magazine.all()[0]
    article = Article(None, "Test Save Article", author.id, magazine.id)
    article.save()
    assert article.id is not None
