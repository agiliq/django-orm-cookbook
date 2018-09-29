중복된 필드 값 갖는 열 찾기
==============================================

.. image:: usertable2.png

:code:`first_name` 이 일치하는 user들을 찾길 원한다고 가정해봅시다. 아래의 쿼리로 중복된 필드 값을 갖는 record들을 찾을 수 있습니다.

.. code-block:: python

    >>> duplicates = User.objects.values(
        'first_name'
        ).annotate(name_count=Count('first_name')).filter(name_count__gt=1)
    >>> duplicates
    <QuerySet [{'first_name': 'John', 'name_count': 3}]>

위의 쿼리에 해당하는 모든 record들의 id를 찾기위해 아래와 같은 쿼리를 쓸 수 있습니다.

.. code-block:: python

    >>> records = User.objects.filter(first_name__in=[item['first_name'] for item in duplicates])
    >>> print([item.id for item in records])
    [2, 11, 13]
