동일한 모델 또는 서로 다른 모델에서 구한 쿼리셋들의 합집합을 구하는 방법은 무엇인가요?
+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

SQL에서는 여러 개의 결과 집합을 합할 때 UNION 연산을 이용합니다. 장고 ORM에서 union 메서드를 이용해 쿼리셋을 합할 수 있습니다. 합하려는 쿼리셋의 모델이 서로 다른 경우, 각 쿼리셋에 포함된 필드와 데이터 유형이 서로 맞아야 합니다.


:code:`auth_user` 모델에서 두 쿼리셋을 구한 뒤 합집합을 구해 봅시다.

.. code-block:: python

    >>> q1 = User.objects.filter(id__gte=5)
    >>> q1
    <QuerySet [<User: Ritesh>, <User: Billy>, <User: Radha>, <User: sohan>, <User: Raghu>, <User: rishab>]>
    >>> q2 = User.objects.filter(id__lte=9)
    >>> q2
    <QuerySet [<User: yash>, <User: John>, <User: Ricky>, <User: sharukh>, <User: Ritesh>, <User: Billy>, <User: Radha>, <User: sohan>, <User: Raghu>]>
    >>> q1.union(q2)
    <QuerySet [<User: yash>, <User: John>, <User: Ricky>, <User: sharukh>, <User: Ritesh>, <User: Billy>, <User: Radha>, <User: sohan>, <User: Raghu>, <User: rishab>]>
    >>> q2.union(q1)
    <QuerySet [<User: yash>, <User: John>, <User: Ricky>, <User: sharukh>, <User: Ritesh>, <User: Billy>, <User: Radha>, <User: sohan>, <User: Raghu>, <User: rishab>]>

다음 코드는 실행하면 오류가 발생합니다.

.. code-block:: python

    >>> q3 = EventVillain.objects.all()
    >>> q3
    <QuerySet [<EventVillain: EventVillain object (1)>]>
    >>> q1.union(q3)
    django.db.utils.OperationalError: SELECTs to the left and right of UNION do not have the same number of result columns


union 메서드는 합하려는 쿼리셋의 필드와 데이터 유형이 서로 일치할 때만 실행할 수 있습니다. 그래서 마지막 명령이 실패했습니다.

:code:`Hero` 모델과 :code:`Villain` 모델은 둘 다 :code:`name` 필드와 :code:`gender` 필드를 갖고 있습니다. :code:`values_list`를 이용해 공통된 필드만 가져온 뒤 union을 수행할 수 있습니다.

... code-block:: python

    Hero.objects.all().values_list(
        "name", "gender"
    ).union(
    Villain.objects.all().values_list(
        "name", "gender"
    ))

위 코드를 실행하면 :code:`Hero` 모델과 :code:`Villain` 모델의 이름과 성별을 함꼐 구할 수 있습니다.

