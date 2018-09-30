필요한 열만 골라 조회하려면 어떻게 하나요?
+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

.. image:: usertable.png

:code:`auth_user` 모델에는 여러 개의 필드가 정의되어 있습니다. 그런데 이 필드가 전부 다 필요하지 않을 때도 있죠. 그럴 때 필요한 열만을 데이터베이스에서 읽어오는 방법을 알아 봅시다.

장고는 두 가지 방법을 제공합니다.

- 쿼리셋의 `values` 메서드와 `values_list` 메서드
- `only` 메서드

이름이 R로 시작하는 모든 사용자의 이름(:code:`first_name`)과 성(:code:`last_name`)을 구해 봅시다. 데이터베이스 시스템의 부하를 줄이기 위해 그 외의 열은 가져오지 않겠습니다.

.. code-block:: python

    >>> User.objects.filter(
        first_name__startswith='R'
    ).values('first_name', 'last_name')
    <QuerySet [{'first_name': 'Ricky', 'last_name': 'Dayal'}, {'first_name': 'Ritesh', 'last_name': 'Deshmukh'}, {'first_name': 'Radha', 'last_name': 'George'}, {'first_name': 'Raghu', 'last_name': 'Khan'}, {'first_name': 'Rishabh', 'last_name': 'Deol'}]

:code:`str(queryset.query)`으로 실제로 실행되는 SQL 질의문을 확인할 수 있습니다. 다음과 같은 질의문이 실행되었습니다.

.. code-block:: sql

    SELECT "auth_user"."first_name", "auth_user"."last_name"
    FROM "auth_user" WHERE "auth_user"."first_name"::text LIKE R%

실행 결과는 사전의 리스트입니다.

한편, only 메서드를 사용할 수도 있습니다.

.. code-block:: python

    >> queryset = User.objects.filter(
        first_name__startswith='R'
    ).only("first_name", "last_name")


:code:`str(queryset.query)`

이 경우 다음과 같은 SQL 질의문을 실행합니다.

.. code-block:: python

    SELECT "auth_user"."id", "auth_user"."first_name", "auth_user"."last_name"
    FROM "auth_user" WHERE "auth_user"."first_name"::text LIKE R%

:code:`only` 메서드가 :code:`values` 메서드와 다른 점은 :code:`id` 필드를 함께 가져온다는 점 뿐입니다.
