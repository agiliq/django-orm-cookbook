How to do OR queries in Django ORM?
++++++++++++++++++++++++++++++++++++++++++++++++++

.. image:: usertable.png

If you are using :code:`django.contrib.auth`, you will have a table called :code:`auth_user`. It will have fields as :code:`username`, :code:`first_name`, :code:`last_name` and more.

A common requirement is performing :code:`OR` filtering with two or more conditions. Say you want to find all users with firstname starting with 'R' and last_name starting with 'D'.

Django provides two options:

- :code:`queryset_1 | queryset_2`
- :code:`filter(Q(<condition_1>)|Q(<condition_2>)`

The query in detail
-----------------------

The SQL query for the above condition will look something like ::

    SELECT username, first_name, last_name, email FROM auth_user WHERE first_name LIKE 'R%' OR last_name LIKE 'D%';

.. image:: sqluser_result1.png

Similarly our ORM query would look like

.. code-block:: python

    queryset = User.objects.filter(
            first_name__startswith='R'
        ) | User.objects.filter(
        last_name__startswith='D'
    )
    queryset
    <QuerySet [<User: Ricky>, <User: Ritesh>, <User: Radha>, <User: Raghu>, <User: rishab>]>

You can also look at the generated query.

.. code-block:: python

    In [5]: str(queryset.query)
    Out[5]: 'SELECT "auth_user"."id", "auth_user"."password", "auth_user"."last_login",
    "auth_user"."is_superuser", "auth_user"."username", "auth_user"."first_name",
    "auth_user"."last_name", "auth_user"."email", "auth_user"."is_staff",
    "auth_user"."is_active", "auth_user"."date_joined" FROM "auth_user"
    WHERE ("auth_user"."first_name"::text LIKE R% OR "auth_user"."last_name"::text LIKE D%)'

Alternatively, you can use the :code:`Q` objects.

.. code-block:: python

    from django.db.models import Q
    qs = User.objects.filter(Q(first_name__startswith='R')|Q(last_name__startswith='D'))

If you look at the generated query, the result is exactly the same

.. code-block:: ipython

    In [9]: str(qs.query)
    Out[9]: 'SELECT "auth_user"."id", "auth_user"."password", "auth_user"."last_login",
     "auth_user"."is_superuser", "auth_user"."username", "auth_user"."first_name",
      "auth_user"."last_name", "auth_user"."email", "auth_user"."is_staff",
      "auth_user"."is_active", "auth_user"."date_joined" FROM "auth_user"
      WHERE ("auth_user"."first_name"::text LIKE R% OR "auth_user"."last_name"::text LIKE D%)'

