How to group records in Django ORM?
========================================

Grouping of records in Django ORM can be done using aggregation functions like :code:`Max`, :code:`Min`, :code:`Avg`, :code:`Sum`. Django queries help to create, retrieve, update and delete objects. But sometimes we need to get aggregated values from the objects. We can get them by example shown below ::

    >>> from django.db.models import Avg, Max, Min, Sum, Count
    >>> User.objects.all().aggregate(Avg('id'))
    {'id__avg': 7.571428571428571}
    >>> User.objects.all().aggregate(Max('id'))
    {'id__max': 15}
    >>> User.objects.all().aggregate(Min('id'))
    {'id__min': 1}
    >>> User.objects.all().aggregate(Sum('id'))
    {'id__sum': 106}
