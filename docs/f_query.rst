필드의 값을 서로 비교하여 항목을 선택할 수 있나요?
==============================================================================

장고 ORM에서 필드를 고정 값과 비교하여 항목을 선택하는 것은 간단합니다. 예를 들어, 이름(:code:`first_name`) 이 :code:`'R'` 로 시작하는 :code:`User` 모델의 행을 구하려면
:code:`User.objects.filter(first_name__startswith='R')` 와 같이 코드를 작성하면 됩니다.

그런데 필드와 필드를 서로 비교할 수도 있을까요? 예를 들어, 이름(:code:`first_name`) 을 성(:code:`last_name`) 과 비교하여 선택하는 것이죠. 이럴 때 :code:`F` 객체를 사용합니다.

실습을 위해 :code:`User` 모델의 항목을 몇 개 생성합시다.

.. code-block:: ipython

    In [27]: User.objects.create_user(email="shabda@example.com", username="shabda", first_name="Shabda", last_name="Raaj")
    Out[27]: <User: shabda>

    In [28]: User.objects.create_user(email="guido@example.com", username="Guido", first_name="Guido", last_name="Guido")
    Out[28]: <User: Guido>

실습 데이터가 준비되었으면, 다음 코드로 이름과 성이 동일한 사용자를 구해 봅시다.


.. code-block:: ipython

    In [29]: User.objects.filter(last_name=F("first_name"))
    Out[29]: <QuerySet [<User: Guido>]>

:code:`F` 객체는 annotate 메서드로 계산해 둔 필드를 가리킬 때도 사용할 수 있습니다. 예를 들어, 이름의 첫 글자와 성의 첫 글자가 동일한 사용자를 구하고 싶다면  :code:`Substr("first_name", 1, 1)` 를 사용할 수 있습니다.

.. code-block:: ipython

    In [41]: User.objects.create_user(email="guido@example.com", username="Tim", first_name="Tim", last_name="Teters")
    Out[41]: <User: Tim>
    #...
    In [46]: User.objects.annotate(first=Substr("first_name", 1, 1), last=Substr("last_name", 1, 1)).filter(first=F("last"))
    Out[46]: <QuerySet [<User: Guido>, <User: Tim>]>

:code:`F` 객체에 :code:`__gt`, :code:`__lt` 등의 룩업(lookup)을 적용하는 것 또한 가능합니다.

