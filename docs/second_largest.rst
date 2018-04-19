How to find second largest record using Django ORM ?
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

You would across situations when you want to find second highest user depending on their age or salary.

Though the ORM gives the flexibility of finding :code:`first()`, :code:`last()` item from the queryset but not nth item. You can do it using the slice operator.

.. image:: usertable.png

We can find Nth records from the query by using slice operator.

.. code-block:: python

    >>> user = User.objects.order_by('-last_login')[1] // Second Highest record w.r.t 'last_login'
    >>> user.first_name
    'Raghu'
    >>> user = User.objects.order_by('-last_login')[2] // Third Highest record w.r.t 'last_login'
    >>> user.first_name
    'Sohan'


:code:`User.objects.order_by('-last_login')[2]` only pulls up the required object from db using :code:`LIMIT ... OFFSET`. If you look at the generated sql, you would see something like this.


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
    ORDER BY "auth_user"."last_login" DESC
    LIMIT 1
    OFFSET 2
