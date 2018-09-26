Annotate된 필드를 어떻게 정렬할 수 있을까요?
==========================================

:code:`Category` 와 :code:`Hero` 모델이 있습니다.

.. code-block:: python

    class Category(models.Model):
        name = models.CharField(max_length=100)


    class Hero(models.Model):
        # ...
        name = models.CharField(max_length=100)
        category = models.ForeignKey(Category, on_delete=models.CASCADE)


:code:`Category` 안에 속한 :code:`Hero` 의 숫자에 따라 정렬하고 싶다면, 다음과 같이 할 수 있습니다.

.. code-block:: python

    Category.objects.annotate(
        hero_count=Count("hero")
    ).order_by(
        "-hero_count"
    )
