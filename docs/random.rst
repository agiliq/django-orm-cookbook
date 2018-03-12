How to select a random object from a model?
========================================================================

For getting a random record from Django's model. We can order_by randomly and fetch the first record.
Example ::

    >>> random_article = Article.objects.order_by('?').first()
    >>> random_article.headline
    'Prime time'
    >>> random_article = Article.objects.order_by('?').first()
    >>> random_article.headline
    'Morning news'

Note: :code:`order_by('?')` queries may be expensive and slow, depending on the database backend you’re using.
