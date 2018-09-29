어떻게 한 모델에서 임의의 객체를 효율적으로 선택할 수 있나요?
========================================================================

:code:`category` 모델이 다음과 같이 정의되어 있습니다.

.. code-block:: python

    class Category(models.Model):
        name = models.CharField(max_length=100)

        class Meta:
            verbose_name_plural = "Categories"

        def __str__(self):
            return self.name


이 Category 모델에서 임의의 객체를 선택하는 몇 가지 방법을 살펴보겠습니다.

가장 직관적인 방법은 임의의 기준으로 정렬(:code:`order_by`)한 뒤에 첫번째 객체를 선택하는 것입니다. 다음과 같이 할 수 있습니다.

.. code-block:: python

    def get_random():
        return Category.objects.order_by("?").first()

참고: :code:`order_by('?')` 쿼리는 사용하고 있는 데이터베이스에 따라 느리고 비효율적일 수 있습니다. 다른 방법을 테스트하기에 앞서서 100만개의 데이터를 :code:`Category` 에 추가해봅시다. :code:`python manage.py dbshell` 과 같은 명령어를 통해 db로 이동하여 다음 구문을 실행합시다.

.. code-block:: sql

    INSERT INTO entities_category
                (name)
    (SELECT Md5(Random() :: text) AS descr
     FROM   generate_series(1, 1000000));

위 코드를 완전히 이해할 필요는 없습니다. 위 코드는 백만개의 숫자를 생성하여 :code:`md5-s` 로 해시한 뒤 그 값을 name에 넣어 db에 저장하는 일을 합니다.

이제 전체 테이블을 정령하지 않고도 max_id를 구한 뒤 [1, max_id]사이의 임의의 숫자를 생성한 뒤 필터링하여 임의의 객체를 선택할 수 있습니다.
다만 이 방법은 db에서 삭제 연산이 없었다는 가정에만 성립합니다.

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

만약 삭제 연산이 있었다면, 유효한 :code:`Category` 객체를 찾을 때까지 반복하도록 코드를 수정하면 됩니다.

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

많은 삭제 연산이 이루어지지 않았다면 :code:`while True:` 는 금세 return할 것입니다. :code:`timeit` 을 사용하여 시간을 비교해봅시다.

.. code-block:: python

    In [14]: timeit.timeit(get_random3, number=100)
    Out[14]: 0.20055226399563253

    In [15]: timeit.timeit(get_random, number=100)
    Out[15]: 56.92513192095794

:code:`get_random3` 가 약 283배나 더 빠르게 나타납니다. :code:`get_random` 이 가장 일반적으로 사용할 수 있는 방법이지만 삭제연산이 많이 이루어지지 않았다면 :code:`get_random3` 의 방법을 사용하는 것이 훨씬 효율적일 수 있습니다.


