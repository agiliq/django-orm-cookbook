어떻게 다른 테이블과 연결된 필드(외래키)를 기준으로 정렬할 수 있을까요?
========================================================================


:code:`Category` 와 :code:`Hero` 모델 두 개가 있습니다.

.. code-block:: python

    class Category(models.Model):
        name = models.CharField(max_length=100)


    class Hero(models.Model):
        # ...
        name = models.CharField(max_length=100)
        category = models.ForeignKey(Category, on_delete=models.CASCADE)

:code:`Hero` 안에 있는 :code:`Hero` 의 이름을 통해 정렬하려면 다음과 같이 할 수 있습니다.

.. code-block:: python

    Hero.objects.all().order_by(
        'category__name', 'name'
    )

:code:`'category__name'`안에 있는 더블 언더스코어(:code:`__` )를 주의 깊게 살펴보세요.
더블 언더스코어를 사용하면, 연결된 모델의 필드를 기준으로 정렬할 수 있습니다.

SQL을 살펴보겠습니다.

.. code-block:: sql

    SELECT "entities_hero"."id",
           "entities_hero"."name",
           -- more fields
    FROM "entities_hero"
    INNER JOIN "entities_category" ON ("entities_hero"."category_id" = "entities_category"."id")
    ORDER BY "entities_category"."name" ASC,
             "entities_hero"."name" ASC
