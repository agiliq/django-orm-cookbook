How to order a queryset in ascending or descending order?
=============================================================

Ordering of the queryset can be achieved by :code:`order_by` method. We need to pass the field on which we need to Order (ascending/descending) the result.
Query looks like this

.. code-block:: ipython

    >>> User.objects.all().order_by('date_joined') # For ascending
    <QuerySet [<User: yash>, <User: John>, <User: Ricky>, <User: sharukh>, <User: Ritesh>, <User: Billy>, <User: Radha>, <User: Raghu>, <User: rishab>, <User: johny>, <User: paul>, <User: johny1>, <User: alien>]>
    >>> User.objects.all().order_by('-date_joined') # For descending; Not '-' sign in order_by method
    <QuerySet [<User: alien>, <User: johny1>, <User: paul>, <User: johny>, <User: rishab>, <User: Raghu>, <User: Radha>, <User: Billy>, <User: Ritesh>, <User: sharukh>, <User: Ricky>, <User: John>, <User: yash>]>

You can pass multiple fields to :code:`order_by`

.. code-block:: ipython

    User.objects.all().order_by('date_joined', '-last_login')

Looking at the SQL


.. code-block:: sql

    SELECT "auth_user"."id",
           -- More fields
           "auth_user"."date_joined"
    FROM "auth_user"
    ORDER BY "auth_user"."date_joined" ASC,
             "auth_user"."last_login" DESC
