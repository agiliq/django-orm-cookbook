How to find distinct field values from queryset?
========================================================================

.. image:: usertable2.png

We can find distinct records from the query as under.::

    >>> distinct = User.objects.values('first_name').annotate(Count('id')).order_by().filter(id__count=1)
    >>> distinct
    <QuerySet [{'id__count': 1, 'first_name': 'Billy'}, {'id__count': 1, 'first_name': 'Paul'}, {'id__count': 1, 'first_name': 'Radha'}, {'id__count': 1, 'first_name': 'Raghu'}, {'id__count': 1, 'first_name': 'Ricky'}, {'id__count': 1, 'first_name': 'Rishabh'}, {'id__count': 1, 'first_name': 'Ritesh'}, {'id__count': 1, 'first_name': 'Sharukh'}, {'id__count': 1, 'first_name': 'Sohan'}, {'id__count': 1, 'first_name': 'Yash'}]>
    >>> records = User.objects.filter(first_name__in=[item['first_name'] for item in distinct])
    >>> print([item.id for item in records])
    [1, 3, 4, 5, 6, 7, 8, 9, 10, 12]