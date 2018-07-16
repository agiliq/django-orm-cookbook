How to use :code:`Q` objects for complex queries?
==================================================

In previous chapters we used :code:`Q` objects for :code:`OR` and :code:`AND` and :code:`NOT` operations. :code:`Q` objects provides you complete control over the where clause of the query.

If you want to :code:`OR` your conditions.

.. code-block:: ipython

    >>> from django.db.models import Q
    >>> queryset = User.objects.filter(
        Q(first_name__startswith='R') | Q(last_name__startswith='D')
    )
    >>> queryset
    <QuerySet [<User: Ricky>, <User: Ritesh>, <User: Radha>, <User: Raghu>, <User: rishab>]>

If you want to :code:`AND` your conditions.

.. code-block:: ipython

    >>> queryset = User.objects.filter(
        Q(first_name__startswith='R') & Q(last_name__startswith='D')
    )
    >>> queryset
    <QuerySet [<User: Ricky>, <User: Ritesh>, <User: rishab>]>

If you want to find all users whose :code:`first_name` starts with 'R', but not if the :code:`last_name` has 'Z'

.. code-block:: ipython

    >>> queryset = User.objects.filter(
        Q(first_name__startswith='R') & ~Q(last_name__startswith='Z')
    )


If you look at the generated query, you would see

.. code-block:: sql

    SELECT "auth_user"."id",
           "auth_user"."password",
           "auth_user"."last_login",
           "auth_user"."is_superuser",
           "auth_user"."username",
           "auth_user"."first_name",
           "auth_user"."last_name",
           "auth_user"."email",
           "auth_user"."is_staff",
           "auth_user"."is_active",
           "auth_user"."date_joined"
    FROM "auth_user"
    WHERE ("auth_user"."first_name"::text LIKE R%
           AND NOT ("auth_user"."last_name"::text LIKE Z%))

You can combine the Q objects in more complex ways to generate complex queries.
