How to do a subquery experession in Django?
=============================================

Django allows using SQL subqueries.
Let's start with something simple, We have a :code:`UserParent` model which has :code:`OnetoOne` relation with auth user. We will find all the :code:`UserParent` which have a :code:`UserParent`.

.. code-block:: ipython

    >>> from django.db.models import Subquery
    >>> users = User.objects.all()
    >>> UserParent.objects.filter(user_id__in=Subquery(users.values('id')))
    <QuerySet [<UserParent: UserParent object (2)>, <UserParent: UserParent object (5)>, <UserParent: UserParent object (8)>]>

Now for something more complex. For each :code:`Category`, we want to find the most benevolent :code:`Hero`.

The models look something like this.

.. code-block:: python

    class Category(models.Model):
        name = models.CharField(max_length=100)


    class Entity(models.Model):
        # ...
        name = models.CharField(max_length=100)
        category = models.ForeignKey(Category, on_delete=models.CASCADE)

        benevolence_factor = models.PositiveSmallIntegerField(
            help_text="How benevolent this hero is?",
            default=50
        )


You can find the most benevolvent Hero like this

.. code-block:: python

    hero_qs = Hero.objects.filter(
        category=OuterRef("pk")
    ).order_by("-benevolence_factor")
    Category.objects.all().annotate(
        most_benevolent_hero=Subquery(
            hero_qs.values('name')[:1]
        )
    )

If you look at the generated sql, you will see

.. code-block:: sql

    SELECT "entities_category"."id",
           "entities_category"."name",

      (SELECT U0."name"
       FROM "entities_hero" U0
       WHERE U0."category_id" = ("entities_category"."id")
       ORDER BY U0."benevolence_factor" DESC
       LIMIT 1) AS "most_benevolent_hero"
    FROM "entities_category"


Let's break down the queryset logic. The first part is

.. code-block:: python

    hero_qs = Hero.objects.filter(
        category=OuterRef("pk")
    ).order_by("-benevolence_factor")

We are ordering the :code:`Hero` object by :code:`benevolence_factor` in DESC order, and using
:code:`category=OuterRef("pk")` to declare that we will be using it in a subquery.

Then we annotate with :code:`most_benevolent_hero=Subquery(hero_qs.values('name')[:1])`, to get use the subquery with a :code:`Category` queryset. The :code:`hero_qs.values('name')[:1]` part picks up the first name from subquery.


