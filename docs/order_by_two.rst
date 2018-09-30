여러 개의 필드를 기준으로 정렬하는 방법이 있나요?
===============================================================================

쿼리셋의 :code:`order_by` 메서드에 여러 개의 정렬 기준 필드를 인자로 전달할 수 있습니다. 그러면 여러 개의 필드를 기준으로 정렬이 수행됩니다.

.. code-block:: ipython

    In [5]: from django.contrib.auth.models import User

    In [6]: User.objects.all().order_by("is_active", "-last_login", "first_name")
    Out[6]: <QuerySet [<User: Guido>, <User: shabda>, <User: Tim>]>
