How to order on a field from a related model (with a foreign key)?
========================================================================


You have two models, :code:`Category` and :code:`Hero`.

.. code-block:: python

    class Category(models.Model):
        name = models.CharField(max_length=100)


    class Hero(models.Model):
        # ...
        name = models.CharField(max_length=100)
        category = models.ForeignKey(Category, on_delete=models.CASCADE)

You want to order :code:`Hero` by category and inside each category by the :code:`Hero` name. You can do.

.. code-block:: python

    Hero.objects.all().order_by(
        'category__name', 'name'
    )

Note the double underscore(:code:`__` ) in :code:`'category__name'`. Using the double undertscore, you can order on a field from a related model.

If you look at the SQL.

.. code-block:: sql

SELECT "entities_hero"."id",
       "entities_hero"."name",
       -- more fields
FROM "entities_hero"
INNER JOIN "entities_category" ON ("entities_hero"."category_id" = "entities_category"."id")
ORDER BY "entities_category"."name" ASC,
         "entities_hero"."name" ASC
