How to perform truncate like operation using Django ORM?
==========================================================

Truncate statement in SQL is mainly meant to deallocate a table, i.e., empty a table for future use.
Though django doesn't provide any such operation https://code.djangoproject.com/ticket/16427, but still similar result can be achived using :code:`delete()` method.
For example:

    >>> Article.objects.all().count()
    7
    >>> Article.objects.all().delete()
    (7, {'events.Article': 7})
    >>> Article.objects.all().count()
    0

From above example it is clear that Article model has no data in it. Which was expected from Truncate statement.