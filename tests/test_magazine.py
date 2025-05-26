import pytest
from lib.db.seed import seed_data
from lib.models.magazine import Magazine
from lib.models.author import Author

@pytest.fixture(scope="module", autouse=True)
def setup_db():
    seed_data()
    yield

def test_magazine_all():
    magazines = Magazine.all()
    assert len(magazines) > 0

def test_find_by_id_name_category():
    mag = Magazine.all()[0]
    found_by_id = Magazine.find_by_id(mag.id)
    assert found_by_id.id == mag.id

    found_by_name = Magazine.find_by_name(mag.name)
    assert found_by_name.name == mag.name

    found_by_category = Magazine.find_by_category(mag.category)
    assert any(m.category == mag.category for m in found_by_category)

def test_articles_relationship():
    mag = Magazine.all()[0]
    articles = mag.articles()
    assert isinstance(articles, list)
    for article in articles:
        assert article.magazine_id == mag.id

def test_contributors():
    mag = Magazine.all()[0]
    contributors = mag.contributors()
    assert isinstance(contributors, list)
    for contributor in contributors:
        assert hasattr(contributor, "name")

def test_article_titles():
    mag = Magazine.all()[0]
    titles = mag.article_titles()
    assert isinstance(titles, list)
    assert all(isinstance(title, str) for title in titles)

def test_contributing_authors():
    mag = Magazine.all()[0]
    authors = mag.contributing_authors()
    assert isinstance(authors, list)
    for author in authors:
        assert hasattr(author, "name")

def test_magazines_with_multiple_authors():
    mags = Magazine.magazines_with_multiple_authors()
    assert isinstance(mags, list)
    assert all(isinstance(m, Magazine) for m in mags)

def test_article_counts():
    counts = Magazine.article_counts()
    assert isinstance(counts, dict)
    for name, count in counts.items():
        assert isinstance(name, str)
        assert isinstance(count, int)

def test_top_publisher():
    top_mag = Magazine.top_publisher()
    assert isinstance(top_mag, Magazine)
    assert hasattr(top_mag, "name")
