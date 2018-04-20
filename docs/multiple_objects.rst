How to create multiple objects in one shot?
++++++++++++++++++++++++++++++++++++++++++++++++++

There are conditions when we want to save multiple objects in one go. Say we want to add multiple categories at once and we don't want to make many queries to the database.
We can use :code:`bulk_create` for creating multiple objects in one shot.

Here is an example.

.. code-block:: ipython

    >>> Category.objects.all().count()
    2
    >>> Category.objects.bulk_create(
        [Category(name="God"),
         Category(name="Demi God"),
         Category(name="Mortal")]
    )
    [<Category: God>, <Category: Demi God>, <Category: Mortal>]
    >>> Category.objects.all().count()
    5

:code:`bulk_create` takes a list of unsaved objects.
