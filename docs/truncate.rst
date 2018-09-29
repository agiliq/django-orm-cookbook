TRUNCATE 문을 수행하는 방법이 있나요?
=============================================================

SQL의 TRUNCATE 문은 표에 저장된 모든 항목을 제거하는 명령입니다. 장고는 TRUNCATE 문을 실행하는 명령을 제공되지 않습니다. 하지만 :code:`delete` 메서드를 이용해 비슷한 결과를 얻을 수 있습니다.

다음 예를 보십시오.

.. code-block:: python

    >>> Category.objects.all().count()
    7
    >>> Category.objects.all().delete()
    (7, {'entity.Category': 7})
    >>> Category.objects.all().count()
    0

위 코드는 잘 동작합니다. 하지만 TRUNCATE 문이 아니라 :code:`DELETE FROM ...`과 같은 SQL 질의를 수행합니다. 삭제해야 하는 항목의 수가 매우 많은 경우 처리 속도가 느릴 수 있습니다. :code:`truncate` 명령이 필요하다면 다음과 같이 :code:`Category` 모델에 :code:`classmethod`로 추가하면 됩니다.


.. code-block:: python

    class Category(models.Model):
        # ...

        @classmethod
        def truncate(cls):
            with connection.cursor() as cursor:
                cursor.execute('TRUNCATE TABLE "{0}" CASCADE'.format(cls._meta.db_table))

이렇게 메서드를 정의해 두면 :code:`Category.truncate()`를 실행하여 정말로 데이터베이스 시스템에 TRUNCATE 문을 질의할 수 있습니다.
