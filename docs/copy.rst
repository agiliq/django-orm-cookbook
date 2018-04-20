How to copy or clone an existing model object?
========================================================================

There is no built-in method for copying model instances, it is possible to create new instance with all fields values copied.

If an instance is saved with instance's :code:`pk` set to :code:`None`, the instance is used to create a new record in the DB. That means every field other than the :code:`PK` is copied.

.. code-block:: ipython

    In [2]: Hero.objects.all().count()
    Out[2]: 4

    In [3]: hero = Hero.objects.first()

    In [4]: hero.pk = None

    In [5]: hero.save()

    In [6]: Hero.objects.all().count()
    Out[6]: 5


