How to solve problems using query related tools?
==================================================

In our previous examples when we did OR'ing and AND'ing of the queries. Similar queries could be done using :code:`Query related tools` ::

    >>> from django.db.models import Q
    >>> queryset = User.objects.filter(Q(first_name__startswith='R') | Q(last_name__startswith='D')) // OR Operation
    >>> queryset
    <QuerySet [<User: Ricky>, <User: Ritesh>, <User: Radha>, <User: Raghu>, <User: rishab>]>
    >>> queryset = User.objects.filter(Q(first_name__startswith='R') & Q(last_name__startswith='D')) // AND Operation
    >>> queryset
    <QuerySet [<User: Ricky>, <User: Ritesh>, <User: rishab>]>

Some other query related tools apart from :code:`Q()` objects are :code:`select_related()` and :code:`prefetch_related()`.
