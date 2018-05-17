How to perform truncate like operation using Django ORM?
==========================================================

Truncate statement in SQL is meant to empty a table for future use.
Though Django doesn't provide a builtin to truncate a table, but still similar result can be achived using :code:`delete()` method.
For example:

.. code-block:: python

    >>> Category.objects.all().count()
    7
    >>> Category.objects.all().delete()
    (7, {'entity.Category': 7})
    >>> Category.objects.all().count()
    0

This works, but this uses :code:`DELETE FROM ...` SQL statement. If you have a large number of records, this can be quite slow. You can add a :code:`classmethod` to :code:`Category` if you want to enable :code:`truncate`.


.. code-block:: python

    class Category(models.Model):
        # ...

        @classmethod
        def truncate(cls):
            with connection.cursor() as cursor:
                cursor.execute('TRUNCATE TABLE "{0}" CASCADE'.format(cls._meta.db_table))

Then you can call :code:`Category.truncate()` to a real database truncate.
