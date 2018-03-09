Find rows which have duplicate field values
==============================================

.. image:: usertable2.png

We can find duplicate records from the query as under.::

    >>> duplicates = User.objects.values('first_name').annotate(Count('id')).order_by().filter(id__count__gt=1)
    >>> duplicates
    <QuerySet [{'first_name': 'John', 'id__count': 3}]>
    >>> records = User.objects.filter(first_name__in=[item['first_name'] for item in duplicates])
    >>> print([item.id for item in records])
    [2, 11, 13]