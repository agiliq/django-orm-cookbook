계산 필드를 기준으로 정렬할 수 있나요?
==========================================================================

:code:`Category` 모델과 :code:`Hero` 모델이 있습니다.

.. code-block:: python

    class Category(models.Model):
        name = models.CharField(max_length=100)


    class Hero(models.Model):
        # ...
        name = models.CharField(max_length=100)
        category = models.ForeignKey(Category, on_delete=models.CASCADE)


:code:`Category` 항목들을 각 :code:`Category` 항목에 속한 :code:`Hero` 항목의 개수에 따라 정렬하고 싶다면, 다음과 같이 :code:`annotate` 메서드로 계산 필드를 준비하여 기준으로 삼을 수 있습니다.

.. code-block:: python

    Category.objects.annotate(
        hero_count=Count("hero")
    ).order_by(
        "-hero_count"
    )
