How to filter a queryset with criteria based on comparing their field values
==============================================================================

Django ORM makes it easy to filter based on fixed values.
To get all :code:`User` objects with :code:`first_name` starting with :code`'R'`,
you can do :code:`User.objects.filter(name_startswith='R')`.

What if you want to compare the first_name and last name?
You can use the :code:`F` object. Create some users first.

.. code-block:: ipython

    In [27]: User.objects.create_user(email="shabda@example.com", username="shabda", first_name="Shabda", last_name="Raaj")
    Out[27]: <User: shabda>

    In [28]: User.objects.create_user(email="guido@example.com", username="Guido", first_name="Guido", last_name="Guido")
    Out[28]: <User: Guido>

Now you can find the users where :code:`first_name==last_name`

.. code-block:: ipython

    In [29]: User.objects.filter(last_name=F("first_name"))
    Out[29]: <QuerySet [<User: Guido>]>

:code:`F` also works with calculated field using annotate. What if we wanted users whose first and last names have same letter?

You can set the first letter from a string using :code:`Substr("first_name", 1, 1)`, so we do.

.. code-block:: ipython

    In [41]: User.objects.create_user(email="guido@example.com", username="Tim", first_name="Tim", last_name="Teters")
    Out[41]: <User: Tim>
    #...
    In [46]: User.objects.annotate(first=Substr("first_name", 1, 1), last=Substr("last_name", 1, 1)).filter(first=F("last"))
    Out[46]: <QuerySet [<User: Guido>, <User: Tim>]>

:code:`F` can also be used with :code:`__gt`, :code:`__lt` and other expressions.
