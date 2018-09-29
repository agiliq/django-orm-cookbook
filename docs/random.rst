모델에서 무작위 항목을 구하는 효율적인 방법이 있을까요?
============================================================================================

:code:`Category` 모델을 아래와 같이 정의했다고 합시다.

.. code-block:: python

    class Category(models.Model):
        name = models.CharField(max_length=100)

        class Meta:
            verbose_name_plural = "Categories"

        def __str__(self):
            return self.name


저장된 Category 항목 가운데 하나를 무작위로 구해야 합니다. 두 가지 방법을 살펴보겠습니다.

먼저 살펴볼 방법은 정직하고 이해하기 쉽습니다. :code:`order_by` 메서드로 항목들을 정렬할 때, 정렬 기준을 '무작위'로 지정하는 것입니다. 데이터를 무작위로 정렬하여 첫 번째 항목을 가져오면 무작위 항목을 구할 수 있습니다. 코드로 작성해 봅시다.

.. code-block:: python

    def get_random():
        return Category.objects.order_by("?").first()

주의: 사용하는 데이터베이스 시스템에 따라 :code:`order_by('?')`의 실행 비용이 비싸고 성능이 느릴 수 있습니다. 뒤이어 살펴볼 다른 방법과의 비교를 위해 :code:`Category` 표에 1백만 개의 항목을 추가해 두겠습니다. 명령행 인터페이스에서  :code:`python manage.py dbshell`를 실행하여 데이터베이스 셸을 열고, 아래 질의문을 실행하시면 실습에 필요한 항목을 준비할 수 있습니다.

.. code-block:: sql

    INSERT INTO entities_category
                (name)
    (SELECT Md5(Random() :: text) AS descr
     FROM   generate_series(1, 1000000));

위 SQL 질의문을 자세히 이해할 필요는 없습니다. (1부터 1백만까지의 수열을 생성하고 난수에 MD5 해시를 적용한 값을 생성하여 데이터베이스에 저장합니다.)

두 번째 방법은 전체 표를 정렬하는 대신 저장된 항목의 마지막 ID를 이용하는 것입니다. 표에서 ID의 최대값을 구하고, 1과 마지막 ID 사이의 난수를 하나 생성합니다. ID가 이 난수와 동일한 항목을 구하면 됩니다.

.. code-block:: python

    In [1]: from django.db.models import Max

    In [2]: from entities.models import Category

    In [3]: import random

    In [4]: def get_random2():
       ...:     max_id = Category.objects.all().aggregate(max_id=Max("id"))['max_id']
       ...:     pk = random.randint(1, max_id)
       ...:     return Category.objects.get(pk=pk)
       ...:

    In [5]: get_random2()
    Out[5]: <Category: e2c3a10d3e9c46788833c4ece2a418e2>

    In [6]: get_random2()
    Out[6]: <Category: f164ad0c5bc8300b469d1c428a514cc1>

이 방법은 항목을 삭제하거나 해서 ID가 중간에 비어있는 경우에는 쓸 수 없습니다. 그런 경우에는 유효한 값이 나올 때까지 반복하도록 하면 됩니다. 다음은 그 방식으로 위의 함수를 수정한 것입니다.

.. code-block:: python

    In [8]: def get_random3():
       ...:     max_id = Category.objects.all().aggregate(max_id=Max("id"))['max_id']
       ...:     while True:
       ...:         pk = random.randint(1, max_id)
       ...:         category = Category.objects.filter(pk=pk).first()
       ...:         if category:
       ...:             return category
       ...:

    In [9]: get_random3()
    Out[9]: <Category: 334aa9926bd65dc0f9dd4fc86ce42e75>

    In [10]: get_random3()
    Out[10]: <Category: 4092762909c2c034e90c3d2eb5a73447>

삭제된 항목이 많지 않다면 위의 무한반복 구문 :code:`while True:`은 금방 종료될 것입니다. 그러면 파이썬의 :code:`timeit`을 이용해 두 방법의 성능 차이를 확인해 봅시다.

.. code-block:: python

    In [14]: timeit.timeit(get_random3, number=100)
    Out[14]: 0.20055226399563253

    In [15]: timeit.timeit(get_random, number=100)
    Out[15]: 56.92513192095794

:code:`get_random3`이 :code:`get_random`보다 283배 빠르게 실행되었습니다. 단, :code:`get_random`은 언제나 이용할 수 있는 반면에, :code:`get_random3`의 방법은 장고의 기본 ID 생성 방식(자동 증가 정수 방식)을 재정의한 경우나 삭제된 항목이 너무 많을 때에는 사용하기가 어려울 수 있습니다.

