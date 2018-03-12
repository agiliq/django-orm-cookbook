How to copy or clone an existing model object?
========================================================================

There is no built-in method for copying model instances, it is possible to easily create new instance with all fields’ values copied. That instance can be saved again by setting instance's :code:`pk` to :code:`None`. For example ::

    >>> Article.objects.all().count()
    5
    >>> reporter = User.objects.get(id = 1)
    >>> reporter
    <User: yash>
    >>> article = Article(headline="Article to test copying instance", pub_date=date(2018, 3, 11), reporter=reporter)
    >>> article.pk
    7
    >>> article.pk = None // Assigning None to pk, to make a copy of an instance.
    >>> article.save()
    >>> article.pk
    8
    >>> Article.objects.all().count()
    7
