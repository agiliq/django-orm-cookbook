How to do union of two querysets from same or different models?
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

The UNION operator is used to combine the result-set of two or more querysets.

Lets continue with our auth_user model and generate 2 querysets to perform union operation ::

    >>> q1 = User.objects.filter(id__gte=5)
    >>> q1
    <QuerySet [<User: Ritesh>, <User: Billy>, <User: Radha>, <User: sohan>, <User: Raghu>, <User: rishab>]>
    >>> q2 = q2 = User.objects.filter(id__lte=9)
    >>> q2
    <QuerySet [<User: yash>, <User: John>, <User: Ricky>, <User: sharukh>, <User: Ritesh>, <User: Billy>, <User: Radha>, <User: sohan>, <User: Raghu>]>
    >>> q1.union(q2)
    <QuerySet [<User: yash>, <User: John>, <User: Ricky>, <User: sharukh>, <User: Ritesh>, <User: Billy>, <User: Radha>, <User: sohan>, <User: Raghu>, <User: rishab>]>
    >>> q2.union(q1)
    <QuerySet [<User: yash>, <User: John>, <User: Ricky>, <User: sharukh>, <User: Ritesh>, <User: Billy>, <User: Radha>, <User: sohan>, <User: Raghu>, <User: rishab>]>

Now try this ::

    >>> q3 = EventVillain.objects.all()
    >>> q3
    <QuerySet [<EventVillain: EventVillain object (1)>]>
    >>> q1.union(q3)
    django.db.utils.OperationalError: SELECTs to the left and right of UNION do not have the same number of result columns


The union operation can be performed only with the querysets having same fields and the datatypes. Hence our last union operation encountered error. You can do a union on two models as long as they have same fields or same subset of fields.

Since :code:`Hero` and :code:`Villain` both have the :code:`name` and :code:`gender`,
we can use :code:`values_list` to limit the selected fields then do a union.


.. code-block:: python

    Hero.objects.all().values_list("name", "gender").union(Villain.objects.all().values_list("name", "gender"))
