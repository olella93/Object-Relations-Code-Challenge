def test_article_save():
    from lib.models.article import Article
    article = Article(title="Test Article", author_id=1, magazine_id=1)
    article.save()
    assert article.id is not None