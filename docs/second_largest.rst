두번째로 큰 항목은 어떻게 구하죠?
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

어떤 필드를 기준으로 데이터를 정렬했을 때, 두 번째 항목을 구해야 하는 경우가 있습니다. 예컨대, 나이·급여 등이 두번째로 많은 사용자를 찾아야 하는 경우가 있겠죠.

장고 ORM에서 첫번째 항목은 :code:`first()` 메서드로, 마지막 항목은 :code:`last()` 메서드로 구할 수 있습니다. 하지만 N번째 항목을 구하는 메서드는 제공되지 않습니다. 그 대신, 파이썬의 인덱싱 연산을 이용할 수 있습니다.

.. image:: usertable.png

아래 코드와 같이, 인덱싱 연산으로 정렬된 데이터의 N번째 항목을 구할 수 있습니다.

.. code-block:: python

    >>> user = User.objects.order_by('-last_login')[1] // Second Highest record w.r.t 'last_login'
    >>> user.first_name
    'Raghu'
    >>> user = User.objects.order_by('-last_login')[2] // Third Highest record w.r.t 'last_login'
    >>> user.first_name
    'Sohan'


:code:`User.objects.order_by('-last_login')[2]` 와 같이 쿼리셋에 인덱스 연산을 지시할 때, 장고 ORM은 데이터베이스에서 전체 데이터를 가져온 뒤 인덱싱하는 것이 아니라, :code:`LIMIT ... OFFSET` SQL 구문을 이용해 필요한 데이터만 읽어 옵니다. 실제로 생성되는 SQL 질의문을 살펴봅시다.

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
