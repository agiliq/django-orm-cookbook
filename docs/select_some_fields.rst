How to select some fields only in a queryset?
++++++++++++++++++++++++++++++++++++++++++++++++++

.. image:: usertable.png

The :code:`auth_user` model has a number of fields in it. But sometimes, you do not need to use all the fields. In such situations, we can query only desired fields.

Django provides two ways to do this

- `values` and `values_list` methods on queryset.
- `only_method`

Say, we want to get :code:`first_name` and :code:`last_name` of all the users whose name starts with **R**. You do not want the fetch the other fields to reduce the work the DB has to do.

.. code-block:: python

    >>> User.objects.filter(
        first_name__startswith='R'
    ).values('first_name', 'last_name')
    <QuerySet [{'first_name': 'Ricky', 'last_name': 'Dayal'}, {'first_name': 'Ritesh', 'last_name': 'Deshmukh'}, {'first_name': 'Radha', 'last_name': 'George'}, {'first_name': 'Raghu', 'last_name': 'Khan'}, {'first_name': 'Rishabh', 'last_name': 'Deol'}]

You can verify the generated sql using :code:`str(queryset.query)`, which gives.

.. code-block:: sql

    SELECT "auth_user"."first_name", "auth_user"."last_name"
    FROM "auth_user" WHERE "auth_user"."first_name"::text LIKE R%

The output will be list of dictionaries.

Alternatively, you can do

.. code-block:: python

    >> queryset = User.objects.filter(
        first_name__startswith='R'
    ).only("first_name", "last_name")


:code:`str(queryset.query)`, gives us

.. code-block:: python

    SELECT "auth_user"."id", "auth_user"."first_name", "auth_user"."last_name"
    FROM "auth_user" WHERE "auth_user"."first_name"::text LIKE R%

The only difference between :code:`only` and :code:`values` is :code:`only` also fetches the :code:`id`.
