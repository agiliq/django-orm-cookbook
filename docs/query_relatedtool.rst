어떻게 복잡한 쿼리에 :code:`Q` 객체를 사용하나요?
==================================================

지난 장에서 :code:`Q` 객체를 :code:`OR` 와 :code:`AND` 그리고 :code:`NOT` 연산에 사용했습니다. :code:`Q` 객체를 사용하면 어떤 쿼리의 Where절을 쉽게 나타낼 수 있습니다.

만약 :code:`OR` 연산을 하고 싶다면,

.. code-block:: ipython

    >>> from django.db.models import Q
    >>> queryset = User.objects.filter(
        Q(first_name__startswith='R') | Q(last_name__startswith='D')
    )
    >>> queryset
    <QuerySet [<User: Ricky>, <User: Ritesh>, <User: Radha>, <User: Raghu>, <User: rishab>]>

만약 :code:`AND` 연산을 하고 싶다면,

.. code-block:: ipython

    >>> queryset = User.objects.filter(
        Q(first_name__startswith='R') & Q(last_name__startswith='D')
    )
    >>> queryset
    <QuerySet [<User: Ricky>, <User: Ritesh>, <User: rishab>]>

만약 이름(:code:`first_name`)이 'R'로 시작하면서 성(:code:`last_name`)은 'Z'로 시작하지 않는 모든 유저를 찾고 싶다면

.. code-block:: ipython

    >>> queryset = User.objects.filter(
        Q(first_name__startswith='R') & ~Q(last_name__startswith='Z')
    )


이때 생성된 쿼리는 다음과 같습니다.

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

더 복잡한 형태의 쿼리들도 Q객체들을 조합하여 얼마든지 나타낼 수 있습니다.
