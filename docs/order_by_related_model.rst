Foreign key로 연결된 모델의 필드로 정렬하려면 어떻게 해야할까?
========================================================================


여기 2개의 모델이 있습니다. :code:`Category` 와 :code:`Hero`.

.. code-block:: python

    class Category(models.Model):
        name = models.CharField(max_length=100)


    class Hero(models.Model):
        # ...
        name = models.CharField(max_length=100)
        category = models.ForeignKey(Category, on_delete=models.CASCADE)

먼저는 category별로 정렬하고 그리고 각 category 내에서 `Hero` 의 name순으로 정렬하려면 이렇게 할 수 있습니다.

.. code-block:: python

    Hero.objects.all().order_by(
        'category__name', 'name'
    )

:code:`'category__name'` 에서 언더스코어 2개( :code:`__` )를 유의하시기 바랍니다. 언더스코어 2개를 이용하면 관계가 있는 모델의 필드로 정렬을 할 수 있습니다.

이와 관련하여 아래 SQL로 나타낼 수 있습니다. 

.. code-block:: sql

    SELECT "entities_hero"."id",
           "entities_hero"."name",
           -- more fields
    FROM "entities_hero"
    INNER JOIN "entities_category" ON ("entities_hero"."category_id" = "entities_category"."id")
    ORDER BY "entities_category"."name" ASC,
             "entities_hero"."name" ASC
