어떻게 두 개의 필드를 정렬할까요?
========================================================================

쿼리셋의 :code:`order_by` 메서드는 하나 이상의 필드의 이름을 가질 수 있습니다. 즉, 두 개 이상의 필드를 기준으로 정렬할 수 있습니다.

..code-block:: ipython

    In [5]: from django.contrib.auth.models import User

    In [6]: User.objects.all().order_by("is_active", "-last_login", "first_name")
    Out[6]: <QuerySet [<User: Guido>, <User: shabda>, <User: Tim>]>
