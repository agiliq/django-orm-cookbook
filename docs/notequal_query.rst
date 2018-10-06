NOT 연산으로 조건을 부정하려면 어떻게 하나요?
++++++++++++++++++++++++++++++++++++++++++++++++++

.. image:: usertable.png

장고의 사용자 계정 관리 앱인 :code:`django.contrib.auth` 를 사용하면 데이터베이스에 :code:`auth_user` 라는 표가 생성됩니다. 이 표에는 :code:`username`, :code:`first_name`, :code:`last_name` 등의 열이 있습니다.

id < 5 라는 조건을 만족하지 않는 모든 사용자를 구해 봅시다. 이를 수행하려면 NOT 연산이 필요합니다.

장고에서는 다음 두 방법으로 구할 수 있습니다.

- :code:`exclude(<condition>)`
- :code:`filter(~Q(<condition>))`


질의문 살펴보기
-----------------------

위 조건의 SQL 질의문은 다음과 같이 생성됩니다. ::

    SELECT id, username, first_name, last_name, email FROM auth_user WHERE NOT id < 5;

.. image:: sqluser_notquery.png

exclude 메서드를 이용하는 방법은 다음과 같습니다. ::

    >>> queryset = User.objects.exclude(id__lt=5)
    >>> queryset
    <QuerySet [<User: Ritesh>, <User: Billy>, <User: Radha>, <User: sohan>, <User: Raghu>, <User: rishab>]>

Q 객체를 이용하는 방법은 다음과 같습니다. ::

    >>> from django.db.models import Q
    >>> queryset = User.objects.filter(~Q(id__lt=5))
    >>> queryst
    <QuerySet [<User: Ritesh>, <User: Billy>, <User: Radha>, <User: sohan>, <User: Raghu>, <User: rishab>]>

