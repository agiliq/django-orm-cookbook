일대다 관계는 어떻게 모델링하는가?
===============================================

관계형 데이터베이스에서는 한 테이블의 상위 레코드가 다른 테이블의 여러 하위 레코드를 참조할 수 있는 경우 일대다 관계가 발생합니다.
일대다 관계에서 상위 레코드가 하위 레코드를 필수적으로 가질 필요는 없습니다. 따라서 일대다 관계는 0개의 하위 레코드, 하나의 하위 레코드 또는 여러 개의 하위 레코드를 허용합니다.
일대다 관계를 정의하려면 ForeignKey를 사용하세요. ::

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

객체를 저장하기 전에 객체를 할당하려고 하면 ValueError가 발생합니다. ::

    >>> u3 = User(username='someuser', first_name='Some', last_name='User', email='some@example.com')
    >>> Article.objects.create(headline="This is a test", pub_date=date(2018, 3, 7), reporter=u1)
    Traceback (most recent call last):
    ...
    ValueError: save() prohibited to prevent data loss due to unsaved related object 'reporter'.
    >>> Article.objects.create(headline="This is a test", pub_date=date(2018, 3, 7), reporter=u1)
    >>> Article.objects.filter(reporter=u1)
    <QuerySet [<Article: This is a test>, <Article: This is a test>]>

위의 쿼리셋은 u1의 여러 개의 :code:`Articles`를 보여줍니다. 따라서 일대다 관계임을 알 수 있습니다.
