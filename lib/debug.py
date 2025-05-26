from lib.models.author import Author
from lib.models.magazine import Magazine
from lib.models.article import Article

# Example: fetch all authors
authors = Author.all()
for author in authors:
    print(f"Author: {author.name}")
    print("Articles:", [article['title'] for article in author.articles()])
    print("Magazines:", [mag['name'] for mag in author.magazines()])
    print("Topic Areas:", author.topic_areas())
    print("------")
