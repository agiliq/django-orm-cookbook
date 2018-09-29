어떻게 두번째로 큰 record를 찾을 수 있나요?
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

연령이나 급여에 따라 두 번째로 높은 사용자를 찾고 싶은 경우가 있습니다.
Django ORM은 :code:`first()` 나 :code:`last()` 와 같은 방식으로 첫번째나 마지막 항목을 찾을 수 있는 유연성을 제공하지만 n번째 항목은 찾을 수 없습니다. 그럴때 slice 연산자를 사용하면 가능합니다

.. image:: usertable.png

slice 연산자를 사용하여 N번째 record를 찾을 수 있습니다.

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
