두번째로 큰 행을 구하려면 어떻게 하나요?
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

예컨대 나이·급여 등이 두번째로 많은 사용자를 찾아야 하는 경우가 있습니다.

장고 ORM에서 첫번째 항목은 :code:`first()` 메서드로, 마지막 항목은 :code:`last()` 메서드로 구할 수 있습니다. 하지만 N번째 항목을 구하는 메서드는 제공되지 않습니다. 그 대신, 파이썬의 인덱싱 연산을 이용하면 됩니다.

.. image:: usertable.png

아래 코드와 같이, 인덱싱 연산을 이용해 정렬된 데이터베이스에서 N번째 항목을 구할 수 있습니다.

.. code-block:: python

    >>> user = User.objects.order_by('-last_login')[1] // Second Highest record w.r.t 'last_login'
    >>> user.first_name
    'Raghu'
    >>> user = User.objects.order_by('-last_login')[2] // Third Highest record w.r.t 'last_login'
    >>> user.first_name
    'Sohan'


:code:`User.objects.order_by('-last_login')[2]` 해당 쿼리는 Database로 부터 세번째로 큰 결과만 가져오는 SQL구문을 생성합니다.
:code:`LIMIT ... OFFSET` 쿼리로 부터 생성된 SQL구문의 LIMIT ... OFFSET 부분을 확인할 수 있습니다.


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
