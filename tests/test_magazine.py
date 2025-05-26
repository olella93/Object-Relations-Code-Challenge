def test_magazine_articles():
    from lib.models.magazine import Magazine
    magazine = Magazine(id=1)
    articles = magazine.articles()
    assert len(articles) >= 1