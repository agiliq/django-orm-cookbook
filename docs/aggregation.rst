Django ORM을 사용하여 어떻게 기록을 집계할 수 있나요?
========================================

:code:`Max`, :code:`Min`, :code:`Avg`, :code:`Sum` 과 같은 집계함수를 사용하면 Django ORM을 사용하여 기록을 집계할 수 있습니다. Django 쿼리를 통해 객체를 생성하고 읽고 갱신하고 삭제할 수 있지만 이 뿐 아니라 기록들을 집계해야 할 때가 있습니다. 다믕과 같은 방법을 통해 기록을 집계할 수 있습니다. ::

    >>> from django.db.models import Avg, Max, Min, Sum, Count
    >>> User.objects.all().aggregate(Avg('id'))
    {'id__avg': 7.571428571428571}
    >>> User.objects.all().aggregate(Max('id'))
    {'id__max': 15}
    >>> User.objects.all().aggregate(Min('id'))
    {'id__min': 1}
    >>> User.objects.all().aggregate(Sum('id'))
    {'id__sum': 106}
