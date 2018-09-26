쿼리셋을 어떻게 오름차순 혹은 내림차순으로 정렬할 수 있을까요?
=============================================================

쿼리셋은 :code:`order_by` 메서드를 사용해서 정렬할 수 있습니다. 오름차순 혹은 내림차순으로 정렬하기 위해선 기준이 되는 필드를 전달해야 합니다.
쿼리는 다음과 같습니다.

.. code-block:: ipython

    >>> User.objects.all().order_by('date_joined') # 오름차순
    <QuerySet [<User: yash>, <User: John>, <User: Ricky>, <User: sharukh>, <User: Ritesh>, <User: Billy>, <User: Radha>, <User: Raghu>, <User: rishab>, <User: johny>, <User: paul>, <User: johny1>, <User: alien>]>
    >>> User.objects.all().order_by('-date_joined') # 내림차순
    <QuerySet [<User: alien>, <User: johny1>, <User: paul>, <User: johny>, <User: rishab>, <User: Raghu>, <User: Radha>, <User: Billy>, <User: Ritesh>, <User: sharukh>, <User: Ricky>, <User: John>, <User: yash>]>

여러개의 필드를 전달할 수도 있습니다.

.. code-block:: ipython

    User.objects.all().order_by('date_joined', '-last_login')

SQL은 다음과 같습니다.


.. code-block:: sql

    SELECT "auth_user"."id",
           -- More fields
           "auth_user"."date_joined"
    FROM "auth_user"
    ORDER BY "auth_user"."date_joined" ASC,
             "auth_user"."last_login" DESC
