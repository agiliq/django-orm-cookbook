일대다 관계는 어떻게 나타내나요?
===================================================

일대다 관계란 한 표의 상위 항목이 다른 표의 여러 하위 항목에서 참조되는 관계입니다. 일대다 관계에서 상위 항목이 반드시 하위 항목을 가진다는 보장은 없습니다. 상위 항목은 하위 항목을 0개, 1개, 여러 개 가질 수 있습니다.

장고 모델에서 일대다 관계를 정의할 때는 :code:`ForeignKey` 필드를 사용합니다.

.. code-block:: python

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

상위 객체를 데이터베이스에 저장하지 않은 채로 하위 객체에 할당하려 하면 :code:`ValueError` 예외가 발생합니다.

>>> u3 = User(username='someuser', first_name='Some', last_name='User', email='some@example.com')
>>> Article.objects.create(headline="This is a test", pub_date=date(2018, 3, 7), reporter=u3)
Traceback (most recent call last):
...
ValueError: save() prohibited to prevent data loss due to unsaved related object 'reporter'.
>>> Article.objects.create(headline="This is a test", pub_date=date(2018, 3, 7), reporter=u1)
>>> Article.objects.filter(reporter=u1)
<QuerySet [<Article: This is a test>, <Article: This is a test>]>

위 코드에서 구한 쿼리셋을 보면, u1 하나에 여러 개의 :code:`Article` 이 연결되어 있음(일대다 관계)을 확인할 수 있습니다.
