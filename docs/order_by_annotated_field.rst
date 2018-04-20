How to order on an annotated field?
==========================================

You have two models, :code:`Category` and :code:`Hero`.

.. code-block:: python

    class Category(models.Model):
        name = models.CharField(max_length=100)


    class Hero(models.Model):
        # ...
        name = models.CharField(max_length=100)
        category = models.ForeignKey(Category, on_delete=models.CASCADE)


You want to get the :code:`Category`, ordered by number of :code:`Hero` in them. You can do this.

.. code-block:: python

    Category.objects.annotate(
        hero_count=Count("hero")
    ).order_by(
        "-hero_count"
    )


