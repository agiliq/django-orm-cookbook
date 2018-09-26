How to find distinct field values from queryset?
어떻게 쿼리셋에서 중복되지 않는 필드 값을 찾나요?
========================================================================

.. image:: usertable2.png

first_name이 중복되지 않는 유저를 찾기위해 아래와 같은 쿼리를 사용할 수 있습니다.

.. code-block:: python

    distinct = User.objects.values(
        'first_name'
    ).annotate(
        name_count=Count('first_name')
    ).filter(name_count=1)
    records = User.objects.filter(first_name__in=[item['first_name'] for item in distinct])

:code:`User.objects.distinct("first_name").all()`, 의 경우 중복된 :code:`first_name` 을 갖는 유저들 중 최초 유저를 가져오므로 위의 쿼리와 차이가 있습니다.

