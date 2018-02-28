How to do NOT EQUAL query in Django queryset?
++++++++++++++++++++++++++++++++++++++++++++++++++

.. image:: usertable.png

Let's say we have a table called auth_user having fields as username, first_name, last_name,  email etc.., and we want to perform NOT operation for fetching users with id NOT < 5.

Our SQL query for the above condition will look somethng like ::

    SELECT id, username, first_name, last_name, email FROM auth_user WHERE NOT id < 5;

.. image:: sqluser_notquery.png

Way 1 using exclude ::

    >>> queryset = User.objects.exclude(id__lt=5)
    >>> queryset
    <QuerySet [<User: Ritesh>, <User: Billy>, <User: Radha>, <User: sohan>, <User: Raghu>, <User: rishab>]>

Way 2 using Q() method aka query tools ::

    >>> from django.db.models import Q
    >>> queryset = User.objects.filter(~Q(id__lt=5))
    >>> queryst
    <QuerySet [<User: Ritesh>, <User: Billy>, <User: Radha>, <User: sohan>, <User: Raghu>, <User: rishab>]>

