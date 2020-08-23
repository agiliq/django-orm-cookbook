How to order on two fields
========================================================================

:code:`order_by` on querysets can take one or more attribute names, allowing you to order on two or more fields.

.. code-block:: ipython

    In [5]: from django.contrib.auth.models import User

    In [6]: User.objects.all().order_by("is_active", "-last_login", "first_name")
    Out[6]: <QuerySet [<User: Guido>, <User: shabda>, <User: Tim>]>

