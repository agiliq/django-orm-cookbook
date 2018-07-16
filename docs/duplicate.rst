Find rows which have duplicate field values
==============================================

.. image:: usertable2.png

Say you want all users whose :code:`first_name` matches another user.

You can find duplicate records using the technique below.

.. code-block:: python

    >>> duplicates = User.objects.values(
        'first_name'
        ).annotate(name_count=Count('first_name')).filter(name_count__gt=1)
    >>> duplicates
    <QuerySet [{'first_name': 'John', 'name_count': 3}]>

If you need to fill all the records, you can do

.. code-block:: python

    >>> records = User.objects.filter(first_name__in=[item['first_name'] for item in duplicates])
    >>> print([item.id for item in records])
    [2, 11, 13]
