장고가 지원하지 않는 데이터베이스 함수를 사용할 수 있나요?
==========================================================================

장고에는 :code:`Lower`, :code:`Coalesce`, :code:`Max` 등의 데이터베이스 함수가 포함되어 있습니다. 하지만 장고가 데이터베이스가 지원하는 모든 함수를 제공하는 것은 아닙니다. 특히, 특정 데이터베이스 시스템의 전용 함수들은 제공되지 않습니다.

장고가 제공하지 않는 데이터베이스 함수를 실행하기 위해서는 장고의 :code:`Func` 객체를 사용하면 됩니다.

PostgreSQL에는 :code:`fuzzystrmatch` 확장 기능이 있습니다. 이 확장에는 텍스트 데이터의 유사도를 측정하기 위한 함수가 여러 가지 포함되어 있습니다. PostgreSQL 데이터베이스 셸에서 :code:`create extension fuzzystrmatch` 를 실행하여 이 확장을 설치하고 아래의 실습을 진행해 주세요.

레벤슈타인 치환 거리 알고리즘을 구현한 :code:`levenshtein` 함수를 이용해 보겠습니다. 실습에 사용할 Hero 모델의 항목을 여러 개 생성합시다.

.. code-block:: python


    Hero.objects.create(name="Zeus", description="A greek God", benevolence_factor=80, category_id=12, origin_id=1)
    Hero.objects.create(name="ZeuX", description="A greek God", benevolence_factor=80, category_id=12, origin_id=1)
    Hero.objects.create(name="Xeus", description="A greek God", benevolence_factor=80, category_id=12, origin_id=1)
    Hero.objects.create(name="Poseidon", description="A greek God", benevolence_factor=80, category_id=12, origin_id=1)

이제 :code:`name` 이 'Zeus' 와 비슷한 :code:`Hero` 항목들을 구해 봅시다.

.. code-block:: python

    from django.db.models import Func, F
    Hero.objects.annotate(like_zeus=Func(F('name'), function='levenshtein', template="%(function)s(%(expressions)s, 'Zeus')"))


:code:`like_zeus=Func(F('name'), function='levenshtein', template="%(function)s(%(expressions)s, 'Zeus')")` 코드에서 :code:`Func` 객체를 세 개의 인자로 초기화하였습니다. 첫 번째 인자는 함수에 적용할 열, 두 번째 인자는 데이터베이스에서 실행할 함수의 이름, 세 번째 인자는 함수를 실행할 SQL 질의문의 템플릿입니다. 이 함수를 여러 번 재사용할 계획이라면 다음과 같이 클래스를 확장하여 정의해 두면 편리합니다.

.. code-block:: python

    class LevenshteinLikeZeus(Func):
        function='levenshtein'
        template="%(function)s(%(expressions)s, 'Zeus')"

이제 :code:`Hero.objects.annotate(like_zeus=LevenshteinLikeZeus(F("name")))` 와 같이 클래스를 이용할 수 있습니다.

이렇게 구한 레벤슈타인 거리를 기준으로 이름이 비슷한 항목을 선별할 수 있습니다.

.. code-block:: ipython

    In [16]: Hero.objects.annotate(
        ...:         like_zeus=LevenshteinLikeZeus(F("name"))
        ...:     ).filter(
        ...:         like_zeus__lt=2
        ...:     )
        ...:
    Out[16]: <QuerySet [<Hero: Zeus>, <Hero: ZeuX>, <Hero: Xeus>]>
