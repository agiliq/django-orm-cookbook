How to model one to many relationships?
===============================================

In relational databases, a one-to-many relationship occurs when a parent record in one table can potentially reference several child records in another table. In a one-to-many relationship, the parent is not required to have child records; therefore, the one-to-many relationship allows zero child records, a single child record or multiple child records.
To define a many-to-one relationship, use `ForeignKey`.::

    class Article(models.Model):
        headline = models.CharField(max_length=100)
        pub_date = models.DateField()
        reporter = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reporter')

        def __str__(self):
            return self.headline

        class Meta:
            ordering = ('headline',)

    >>> u1 = User(username='johny1', first_name='Johny', last_name='Smith', email='johny@example.com')
    >>> u1.save()
    >>> u2 = User(username='alien', first_name='Alien', last_name='Mars', email='alien@example.com')
    >>> u2.save()
    >>> from datetime import date
    >>> a1 = Article(headline="This is a test", pub_date=date(2018, 3, 6), reporter=u1)
    >>> a1.save()
    >>> a1.reporter.id
    13
    >>> a1.reporter
    <User: johny1>

If you try to assign an object before saving it you will encounter a ValueError ::

    >>> u3 = User(username='someuser', first_name='Some', last_name='User', email='some@example.com')
    >>> Article.objects.create(headline="This is a test", pub_date=date(2018, 3, 7), reporter=u3)
    Traceback (most recent call last):
    ...
    ValueError: save() prohibited to prevent data loss due to unsaved related object 'reporter'.
    >>> Article.objects.create(headline="This is a test", pub_date=date(2018, 3, 7), reporter=u1)
    >>> Article.objects.filter(reporter=u1)
    <QuerySet [<Article: This is a test>, <Article: This is a test>]>

The above queryset shows User u1 with multiple :code:`Articles`. Hence One to Many.
