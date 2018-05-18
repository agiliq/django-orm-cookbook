How to create a generic model which can be related to any kind of entity? (Eg. a Category or a Comment?)
=============================================================================================================


You have models like this.

.. code-block:: python

    class Category(models.Model):
        name = models.CharField(max_length=100)
        # ...

        class Meta:
            verbose_name_plural = "Categories"


    class Hero(models.Model):
        name = models.CharField(max_length=100)
        category = models.ForeignKey(Category, on_delete=models.CASCADE)
        # ...


    class Villain(models.Model):
        name = models.CharField(max_length=100)
        category = models.ForeignKey(Category, on_delete=models.CASCADE)
        # ...


:code:`Category` can be applied is a `generic` model. You prbably want to be able to apply categories to objects form any model class.
You can do it like this


.. code-block:: python

    from django.contrib.contenttypes.fields import GenericForeignKey
    from django.contrib.contenttypes.models import ContentType
    # ...

    class FlexCategory(models.Model):
        name = models.SlugField()
        content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
        object_id = models.PositiveIntegerField()
        content_object = GenericForeignKey('content_type', 'object_id')


    class Hero(models.Model):
        name = models.CharField(max_length=100)
        flex_category = GenericRelation(FlexCategory, related_query_name='flex_category')
        # ...


    class Villain(models.Model):
        name = models.CharField(max_length=100)
        flex_category = GenericRelation(FlexCategory, related_query_name='flex_category')
        # ...


What did we do, we added we added a :code:`GenericForeignKey` fields on :code:`FlexCategory` using one :code:`ForeignKey` and one :code:`PositiveIntegerField`, then
added a :code:`GenericRelation` on the models you want to categorize.


At the database level it looks like this:

.. code-block

         Column      |         Type          |                             Modifiers
    -----------------+-----------------------+--------------------------------------------------------------------
     id              | integer               | not null default nextval('entities_flexcategory_id_seq'::regclass)
     name            | character varying(50) | not null
     object_id       | integer               | not null
     content_type_id | integer               | not null


You can categorize a :code:`Hero` like this.


.. code-block:: python

    FlexCategory.objects.create(content_object=hero, name="mythic")

And then get a :code:`Hero` categorised as 'ghost' like this

.. code-block:: python

    FlexCategory.objects.create(content_object=hero, name="mythic")

This gives us this sql.

.. code-block:: sql


    SELECT "entities_hero"."name"
    FROM "entities_hero"
    INNER JOIN "entities_flexcategory" ON ("entities_hero"."id" = "entities_flexcategory"."object_id"
                                           AND ("entities_flexcategory"."content_type_id" = 8))
    WHERE "entities_flexcategory"."name" = ghost
