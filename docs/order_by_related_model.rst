외래 키로 연결된 다른 표의 열을 기준으로 정렬할 수 있나요?
==========================================================================

:code:`Category` 모델과 :code:`Hero` 모델이 다음과 같이 외래 키(ForeignKey)로 연결되어 있습니다.

.. code-block:: python

    class Category(models.Model):
        name = models.CharField(max_length=100)


    class Hero(models.Model):
        # ...
        name = models.CharField(max_length=100)
        category = models.ForeignKey(Category, on_delete=models.CASCADE)

아래 코드는 :code:`Hero` 모델의 쿼리셋을 category 필드 순으로 정렬하되, category가 같은 항목은 (:code:`Hero`의) name 필드 순으로 정렬합니다.


.. code-block:: python

    Hero.objects.all().order_by(
        'category__name', 'name'
    )

:code:`'category__name'` 인자에 이중 밑줄 기호(:code:`__` )를 사용한 것을 봐 주세요. 이중 밑줄 기호로 연결된 모델의 필드를 가리킬 수 있습니다.

SQL 질의문은 다음과 같이 생성됩니다.

.. code-block:: sql

    SELECT "entities_hero"."id",
           "entities_hero"."name",
           -- more fields
    FROM "entities_hero"
    INNER JOIN "entities_category" ON ("entities_hero"."category_id" = "entities_category"."id")
    ORDER BY "entities_category"."name" ASC,
             "entities_hero"."name" ASC

