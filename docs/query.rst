장고 ORM이 실행하는 실제 SQL 질의문을 확인할 수 있나요?
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

장고 ORM이 실행하는 질의문 또는 우리가 작성한 코드에 대응하는 SQL 질의문이 무엇인지 확인하고 싶을 때가 있습니다. SQL 질의문을 구하고 싶은 :code:`queryset.query`의 :code:`str`을 확인하면 됩니다. 간단하죠?

:code:`Event`라는 모델이 있을 때, 이 모델의 모든 행을 데이터베이스에서 읽어오려면 :code:`Event.objects.all()`과 같은 코드를 작성하면 됩니다. 이렇게 구한 쿼리셋의 :code:`str(queryset.query)`를 확인하여 SQL 질의문을 살펴봅시다.

.. code-block:: python

    >>> queryset = Event.objects.all()
    >>> str(queryset.query)
    SELECT "events_event"."id", "events_event"."epic_id",
        "events_event"."details", "events_event"."years_ago"
        FROM "events_event"

.. image:: sql_query.png

두 번째 예제

.. code-block:: python

    >>> queryset = Event.objects.filter(years_ago__gt=5)
    >>> str(queryset.query)
    SELECT "events_event"."id", "events_event"."epic_id", "events_event"."details",
    "events_event"."years_ago" FROM "events_event"
    WHERE "events_event"."years_ago" > 5

