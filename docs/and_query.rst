How to do AND queries in Django ORM?
++++++++++++++++++++++++++++++++++++++++++++++++++

.. image:: usertable.png

If you are using :code:`django.contrib.auth`, you will have a table called :code:`auth_user`. It will have fields as :code:`username`, :code:`first_name`, :code:`last_name` and more.


You qould frequnenty need to want to perform AND operation, to find querysets which match multiple criteria.

Say you want to find users with :code:`firstname` starting with 'R' AND :code:`last_name` starting with 'D'.

Django provides three options.

- :code:`filter(<condition_1>, <condition_2>)`
- :code:`queryset_1 & queryset_2`
- :code:`filter(Q(<condition_1>) & Q(<condition_2>))`


The query in detail
-----------------------


Our SQL query for the above condition will look something like

.. code-block:: sql

    SELECT username, first_name, last_name, email FROM auth_user WHERE first_name LIKE 'R%' AND last_name LIKE 'D%';

.. image:: sqluser_result2.png

The default way to combine multiple conditions in :code:`filter` is :code:`AND`, so you can just do.

.. code-block:: python

    queryset_1 = User.objects.filter(
        first_name__startswith='R',
        last_name__startswith='D'
    )

Alternatively, you can explicitly use the `&` operator on querysets.

.. code-block:: python

    queryset_2 = User.objects.filter(
        first_name__startswith='R'
    ) & User.objects.filter(
        last_name__startswith='D'
    )

For complete customisibility, you can use the :code:`Q` objects.

.. code-block:: python

    queryset_3 = User.objects.filter(
        Q(first_name__startswith='R') &
        Q(last_name__startswith='D')
    )


    queryset_1
    <QuerySet [<User: Ricky>, <User: Ritesh>, <User: rishab>]>

You can look at the generated query and verify that they are all same.

.. code-block:: ipython

    In [10]: str(queryset_2.query)
    Out[10]: 'SELECT "auth_user"."id", "auth_user"."password", "auth_user"."last_login", "auth_user"."is_superuser", "auth_user"."username", "auth_user"."first_name", "auth_user"."last_name", "auth_user"."email", "auth_user"."is_staff", "auth_user"."is_active", "auth_user"."date_joined" FROM "auth_user" WHERE ("auth_user"."first_name"::text LIKE R% AND "auth_user"."last_name"::text LIKE D%)'

    In [11]: str(queryset_1.query) == str(queryset_2.query) == str(queryset_3.query)
    Out[11]: True
