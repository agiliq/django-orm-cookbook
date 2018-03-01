How to select some fields only in a queryset?
++++++++++++++++++++++++++++++++++++++++++++++++++

.. image:: usertable.png

We have a auth_user model having some 5 fields in it. But sometimes we are not in need to use all the fields so for such situations we can query only desired fields.
This can be achieved my ``values`` method.

Say, we want to get firstname and lastname off all the users having initials as **R** ::

    >>> User.objects.filter(first_name__startswith='R').values('first_name', 'last_name')
    <QuerySet [{'first_name': 'Ricky', 'last_name': 'Dayal'}, {'first_name': 'Ritesh', 'last_name': 'Deshmukh'}, {'first_name': 'Radha', 'last_name': 'George'}, {'first_name': 'Raghu', 'last_name': 'Khan'}, {'first_name': 'Rishabh', 'last_name': 'Deol'}]

The output will be list of dictionaries with desired result.