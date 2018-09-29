항목들을 집계하는 방법은 무엇인가요?
===========================================

장고 ORM을 이용해 항목을 생성·조회·갱신·삭제할 수 있지만, 때로는 항목들의 집계값을 구하고 싶을 때가 있습니다. 장고 ORM에는 SQL의 일반적인 집계 기능을 수행하는 :code:`Max`, :code:`Min`, :code:`Avg`, :code:`Sum` 등의 함수가 있습니다. 다음은 이 집계 함수를 이용하는 예입니다. ::

    >>> from django.db.models import Avg, Max, Min, Sum, Count
    >>> User.objects.all().aggregate(Avg('id'))
    {'id__avg': 7.571428571428571}
    >>> User.objects.all().aggregate(Max('id'))
    {'id__max': 15}
    >>> User.objects.all().aggregate(Min('id'))
    {'id__min': 1}
    >>> User.objects.all().aggregate(Sum('id'))
    {'id__sum': 106}
