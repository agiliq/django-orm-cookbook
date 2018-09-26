필드 값 비교를 기준으로 쿼리셋 필터링 하기
==============================================================================

Django ORM은 고정된 값으로 필터링하는 것을 도와줍니다.
:code:`first_name` 이 :code:`'R'` 로 시작하는 :code:`User` Object를 얻기 위해 
:code:`User.objects.filter(first_name__startswith='R')` 를 쓸 수 있습니다.
만약 first_name과 last_name을 비교하고 싶다면 :code:`F` obejct를 쓸 수 있습니다.
먼저 user를 만들어보겠습니다.


.. code-block:: ipython

    In [27]: User.objects.create_user(email="shabda@example.com", username="shabda", first_name="Shabda", last_name="Raaj")
    Out[27]: <User: shabda>

    In [28]: User.objects.create_user(email="guido@example.com", username="Guido", first_name="Guido", last_name="Guido")
    Out[28]: <User: Guido>

이제 fisrt_name과 last_name이 같은 유저를 찾을 수 있습니다.


.. code-block:: ipython

    In [29]: User.objects.filter(last_name=F("first_name"))
    Out[29]: <QuerySet [<User: Guido>]>

:code:`F` object는 annotate를 사용하여 계산된 필드에서도 사용할 수 있습니다.
만약 first_name과 last_name의 첫글자가 같은 유저를 찾길 원한다면 :code:`Substr("first_name", 1, 1)` 를 사용할 수 있습니다.

.. code-block:: ipython

    In [41]: User.objects.create_user(email="guido@example.com", username="Tim", first_name="Tim", last_name="Teters")
    Out[41]: <User: Tim>
    #...
    In [46]: User.objects.annotate(first=Substr("first_name", 1, 1), last=Substr("last_name", 1, 1)).filter(first=F("last"))
    Out[46]: <QuerySet [<User: Guido>, <User: Tim>]>

또한 :code:`F` object는 :code:`__gt`, :code:`__lt` 나 다른 expression과 함께 사용 가능합니다.

