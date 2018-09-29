어떻게 쿼리셋에서 데이터베이스의 특정한 함수를 사용할 수 있나요?
========================================================================

Django에서도 :code:`Lower`, :code:`Coalesce`, :code:`Max` 와 같은 함수를 제공하지만 모든 데이터베이스의 함수를 제공하지는 않습니다. 각 데이터베이스의 특징적인 함수들은 더욱 더 그렇습니다.

Django에서는 Django에서 제공하지 않는 특정한 데이터베이스 함수를 사용할 수 있게 해주는 :code:`Func` 함수를 제공합니다.


Postgres는 유사성을 측정하는 몇가지 함수의 모음인 :code:`fuzzystrmatch` 가 있습니다. :code:`create extension fuzzystrmatch` 명령으로 postgres DB에 이를 설치할 수 있습니다.

Postgres의 :code:`levenshtein` 함수를 사용해봅시다. 먼저 Hero 객체를 몇 개 만들어 봅시다.

.. code-block:: python


    Hero.objects.create(name="Zeus", description="A greek God", benevolence_factor=80, category_id=12, origin_id=1)
    Hero.objects.create(name="ZeuX", description="A greek God", benevolence_factor=80, category_id=12, origin_id=1)
    Hero.objects.create(name="Xeus", description="A greek God", benevolence_factor=80, category_id=12, origin_id=1)
    Hero.objects.create(name="Poseidon", description="A greek God", benevolence_factor=80, category_id=12, origin_id=1)

이 때 이름(:code:`name`)이 Zeus와 유사한 :code:`Hero` 객체를 찾고 싶다면 다음과 같이 할 수 있습니다.

.. code-block:: python

    from django.db.models import Func, F
    Hero.objects.annotate(like_zeus=Func(F('name'), function='levenshtein', template="%(function)s(%(expressions)s, 'Zeus')"))


:code:`like_zeus=Func(F('name'), function='levenshtein', template="%(function)s(%expressions)s, 'Zeus')")` 는 function과 template, 두 인자를 받습니다. 만약 이 함수를 재사용하고 싶다면 다음과 같은 클래스를 정의하면 됩니다.

.. code-block:: python

    class LevenshteinLikeZeus(Func):
        function='levenshtein'
        template="%(function)s(%(expressions)s, 'Zeus')"

이제 이것을 :code:`Hero.objects.annotate(like_zeus=LevenshteinLikeZeus(F("name")))` 과 같이 사용하면 됩니다.

이렇게 생성된 :code:`like_zeus` 필드를 다음과 같이 필터링할 수 있습니다.

.. code-block:: ipython

    In [16]: Hero.objects.annotate(
        ...:         like_zeus=LevenshteinLikeZeus(F("name"))
        ...:     ).filter(
        ...:         like_zeus__lt=2
        ...:     )
        ...:
    Out[16]: <QuerySet [<Hero: Zeus>, <Hero: ZeuX>, <Hero: Xeus>]>
