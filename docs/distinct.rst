How to find distinct field values from queryset?
========================================================================

.. image:: usertable2.png

You want to find users whose names have not been repeated. You can do this like this

.. code-block:: python

    distinct = User.objects.values(
        'first_name'
    ).annotate(
        name_count=Count('first_name')
    ).filter(name_count=1)
    records = User.objects.filter(first_name__in=[item['first_name'] for item in distinct])

This is different from :code:`User.objects.distinct("first_name").all()`, which will pull up the first record when it encounters a distinct :code:`first_name`.


