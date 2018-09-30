쿼리셋에서 고유한 필드 값을 가진 항목은 어떻게 구하나요?
========================================================================

.. image:: usertable2.png

이름이 다른 사용자와 겹치지 않은 사용자를 찾는다고 합시다. 다음과 같이 구할 수 있습니다.

.. code-block:: python

    distinct = User.objects.values(
        'first_name'
    ).annotate(
        name_count=Count('first_name')
    ).filter(name_count=1)
    records = User.objects.filter(first_name__in=[item['first_name'] for item in distinct])

한편, :code:`User.objects.distinct("first_name").all()`와 같은 코드는 고유한 :code:`first_name`을 가진 사용자별로 첫번째 사용자를 구하는 코드입니다. 위 코드와는 실행 결과가 다릅니다.

