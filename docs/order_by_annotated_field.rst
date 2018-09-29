주석처리된(annotated) 필드를 어떻게 정렬할 수 있을까?
==========================================

여기 2개의 모델이 있습니다. :code:`Category` 와 :code:`Hero`.

.. code-block:: python

    class Category(models.Model):
        name = models.CharField(max_length=100)


    class Hero(models.Model):
        # ...
        name = models.CharField(max_length=100)
        category = models.ForeignKey(Category, on_delete=models.CASCADE)


:code:`Hero` 가 많은 순서대로 :code:`Category` 를 얻고 싶다면 이렇게 하면 됩니다.

.. code-block:: python

    Category.objects.annotate(
        hero_count=Count("hero")
    ).order_by(
        "-hero_count"
    )


