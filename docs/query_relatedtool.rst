Q 객체를 이용해 복잡한 질의를 수행하는 방법은 무엇인가요?
====================================================================

앞선 몇 개의 장에서 :code:`Q` 객체를 이용해 :code:`OR` 연산, :code:`AND` 연산, :code:`NOT` 연산을 수행해 보았습니다. :code:`Q` 객체를 이용하면 SQL 질의문의 WHERE 절에 해당하는 기능을 온전히 활용할 수 있습니다.

조건식에서 :code:`OR` 연산을 수행하려면 다음과 같이 합니다.

.. code-block:: ipython

    >>> from django.db.models import Q
    >>> queryset = User.objects.filter(
        Q(first_name__startswith='R') | Q(last_name__startswith='D')
    )
    >>> queryset
    <QuerySet [<User: Ricky>, <User: Ritesh>, <User: Radha>, <User: Raghu>, <User: rishab>]>

조건식에서 :code:`AND` 연산을 수행하려면 다음과 같이 합니다.

.. code-block:: ipython

    >>> queryset = User.objects.filter(
        Q(first_name__startswith='R') & Q(last_name__startswith='D')
    )
    >>> queryset
    <QuerySet [<User: Ricky>, <User: Ritesh>, <User: rishab>]>

이름(:code:`first_name`)이 'R'로 시작하되, 성(:code:`last_name`)에 'Z'가 포함되지 않은 사용자를 모두 구하려면 다음과 같이 조건을 작성하면 됩니다.

.. code-block:: ipython

    >>> queryset = User.objects.filter(
        Q(first_name__startswith='R') & ~Q(last_name__startswith='Z')
    )

위 코드로 생성되는 질의문은 다음과 같습니다.

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

Q 객체를 이용하면 이보다 더 복잡한 조건의 질의도 문제 없이 지시할 수 있습니다.
