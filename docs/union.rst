같은 모델 또는 다른 모델에서의 2개의 쿼리셋을 어떻게 합칠까(union)?
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

union은 2개 이상의 쿼리셋 결과물을 합칠 때 사용됩니다.
쿼리셋은 같거나 다른 모델에서 만들 수 있습니다. 만약 다른 모델을 통해 얻은 쿼리셋이라면, 필드와 데이터 타입을 맞춰야만 합니다.

:code:`auth_user` 을 통해 계속 보도록 합시다. 이 모델로부터 union을 하기 위해 2개의 쿼리셋을 생성하겠습니다.

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

자, 해봅시다.

.. code-block:: python

    >>> q3 = EventVillain.objects.all()
    >>> q3
    <QuerySet [<EventVillain: EventVillain object (1)>]>
    >>> q1.union(q3)
    django.db.utils.OperationalError: SELECTs to the left and right of UNION do not have the same number of result columns


union은 오직 같은 필드와 같은 데이터타입을 갖는 쿼리셋으로 실행할 수 있습니다. 그렇기 때문에 위 마지막에 error를 만나게 된 겁니다. 같은 필드 쿼리셋이면 2개 모델에서 union을 실행할 수 있습니다.

:code:`Hero` 와 :code:`Villain` 두 개 모델 모두 :code:`name` 과 :code:`gender` 를 가지고 있기 때문에
우리는 2개 필드로 제한하기 위해 :code:`values_list` 를 사용한 후 union을 할 수 있습니다.


.. code-block:: python

    Hero.objects.all().values_list(
        "name", "gender"
    ).union(
    Villain.objects.all().values_list(
        "name", "gender"
    ))

위 코드를 통해 :code:`Hero` 와 :code:`Villain` 모델의 name과 gender 모두를 얻게 될 것입니다.
