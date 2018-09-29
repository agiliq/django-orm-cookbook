여러 조건을 OR 연산하여 데이터를 걸러내려면 어떻게 하나요?
++++++++++++++++++++++++++++++++++++++++++++++++++++

.. image:: usertable.png

장고의 사용자 계정 관리 앱인 :code:`django.contrib.auth`를 사용하면 데이터베이스에 :code:`auth_user`이라는 표가 생성됩니다. 이 표에는 :code:`username`, :code:`first_name`, :code:`last_name` 등의 열이 있습니다.

데이터를 걸러낼 때, 두 가지 이상의 조건을 :code:`OR` 연산하여야 하는 경우가 많습니다. 이름이 'R'로 시작하거나 성이 'D'로 시작하는 모든 사용자를 구한다고 해 봅시다.

장고에서는 다음 두 방법으로 구할 수 있습니다.

- :code:`queryset_1 | queryset_2`
- :code:`filter(Q(<condition_1>)|Q(<condition_2>)`


질의문 살펴보기
-----------------------

위 조건의 SQL 질의문은 대략 다음과 같습니다. ::

    SELECT username, first_name, last_name, email FROM auth_user WHERE first_name LIKE 'R%' OR last_name LIKE 'D%';

.. image:: sqluser_result1.png

장고 ORM 코드도 비슷합니다.

.. code-block:: python

    queryset = User.objects.filter(
            first_name__startswith='R'
        ) | User.objects.filter(
        last_name__startswith='D'
    )
    queryset
    <QuerySet [<User: Ricky>, <User: Ritesh>, <User: Radha>, <User: Raghu>, <User: rishab>]>

장고 ORM이 생성하는 SQL 질의문도 한 번 확인해 봅시다.

.. code-block:: python

    In [5]: str(queryset.query)
    Out[5]: 'SELECT "auth_user"."id", "auth_user"."password", "auth_user"."last_login",
    "auth_user"."is_superuser", "auth_user"."username", "auth_user"."first_name",
    "auth_user"."last_name", "auth_user"."email", "auth_user"."is_staff",
    "auth_user"."is_active", "auth_user"."date_joined" FROM "auth_user"
    WHERE ("auth_user"."first_name"::text LIKE R% OR "auth_user"."last_name"::text LIKE D%)'

:code:`Q` 객체를 이용하는 방법도 가능합니다.

.. code-block:: python

    from django.db.models import Q
    qs = User.objects.filter(Q(first_name__startswith='R')|Q(last_name__startswith='D'))

두 방법 모두 생성되는 SQL 질의문은 완전히 동일합니다.

.. code-block:: ipython

    In [9]: str(qs.query)
    Out[9]: 'SELECT "auth_user"."id", "auth_user"."password", "auth_user"."last_login",
     "auth_user"."is_superuser", "auth_user"."username", "auth_user"."first_name",
      "auth_user"."last_name", "auth_user"."email", "auth_user"."is_staff",
      "auth_user"."is_active", "auth_user"."date_joined" FROM "auth_user"
      WHERE ("auth_user"."first_name"::text LIKE R% OR "auth_user"."last_name"::text LIKE D%)'

