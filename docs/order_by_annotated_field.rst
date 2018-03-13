How to order on an annotated field?
==========================================

Here we will talk about two models i.e., :code:`Article` and :code:`User`. Article has FK relationship with User model. Here we will be counting the articles created by user and order them in ascending order. ::


    >>> from django.db.models import Sum
    >>> Article.objects.values('reporter__username').annotate(reporter_article = Sum('reporter')).order_by('reporter_article')
    <QuerySet [{'reporter_article': 2, 'reporter__username': 'yash'},
     {'reporter_article': 10, 'reporter__username': 'John'},
      {'reporter_article': 11, 'reporter__username': 'johny'}]>