어떻게 하면 2개의 필드를 기준으로 정렬할 수 있을까?
========================================================================

쿼리셋에서 :code:`order_by`는 1개 내지는 그 이상의 필드로 정렬을 가능하게 해줍니다.

..code-block:: ipython

    In [5]: from django.contrib.auth.models import User

    In [6]: User.objects.all().order_by("is_active", "-last_login", "first_name")
    Out[6]: <QuerySet [<User: Guido>, <User: shabda>, <User: Tim>]>

