def test_author_articles():
    from lib.models.author import Author
    author = Author.find_by_id(1)
    articles = author.articles()
    assert len(articles) >= 1

def test_author_magazines():
    from lib.models.author import Author
    author = Author.find_by_id(1)
    magazines = author.magazines()
    assert len(magazines) >= 1