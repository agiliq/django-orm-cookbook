How to use arbitrary database functions in querysets?
========================================================================

Django comes with functions like :code:`Lower`, :code:`Coalesce` and :code:`Max`, but it can't support all database functions, expecially ones which are database specific.

Django provides :code:`Func` which allows using arbitrary database functions, even if Django doesn't provide them.


Postgres has :code:`fuzzystrmatch`, which provides several functions to determine similarities. Install; the extension in your postgres DB with :code:`create extension fuzzystrmatch`

We will use the :code:`levenshtein` function. Lets first create some Hero objects.

.. code-block:: python


    Hero.objects.create(name="Zeus", description="A greek God", benevolence_factor=80, category_id=12, origin_id=1)
    Hero.objects.create(name="ZeuX", description="A greek God", benevolence_factor=80, category_id=12, origin_id=1)
    Hero.objects.create(name="Xeus", description="A greek God", benevolence_factor=80, category_id=12, origin_id=1)
    Hero.objects.create(name="Poseidon", description="A greek God", benevolence_factor=80, category_id=12, origin_id=1)

We want to find out the :code:`Hero` objects which have :code:`name` similar to Zeus. You can do

.. code-block:: python

    from django.db.models import Func, F
    Hero.objects.annotate(like_zeus=Func(F('name'), function='levenshtein', template="%(function)s(%(expressions)s, 'Zeus')"))


The :code:`like_zeus=Func(F('name'), function='levenshtein', template="%(function)s(%(expressions)s, 'Zeus')")` took two arguments which allowed the database representation, viz, :code:`function` and :code:`template`. If you need to reuse the function, you can define a class like this.

.. code-block:: python

    class LevenshteinLikeZeus(Func):
        function='levenshtein'
        template="%(function)s(%(expressions)s, 'Zeus')"

And then use :code:`Hero.objects.annotate(like_zeus=LevenshteinLikeZeus(F("name")))`

You can then filter on this annotated field like this.

.. code-block:: ipython

    In [16]: Hero.objects.annotate(
        ...:         like_zeus=LevenshteinLikeZeus(F("name"))
        ...:     ).filter(
        ...:         like_zeus__lt=2
        ...:     )
        ...:
    Out[16]: <QuerySet [<Hero: Zeus>, <Hero: ZeuX>, <Hero: Xeus>]>
