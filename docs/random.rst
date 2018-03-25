How to efficiently select a random object from a model?
========================================================================

Your :code:`category` models is like this.

.. code-block:: python

    class Category(models.Model):
        name = models.CharField(max_length=100)

        class Meta:
            verbose_name_plural = "Categories"

        def __str__(self):
            return self.name


You want to get a random Category. We will look at few alternate ways to do this.

The most straightforward way, you can order_by random and fetch the first record. It would look something like this.

.. code-block:: python

    def get_random():
        return Category.objects.order_by("?").first()

Note: :code:`order_by('?')` queries may be expensive and slow, depending on the database backend you’re using. To test other methods, we need to instert one million records in :code:`Category` table. Go to your db like with :code:`python manage.py dbshell` and run this.

.. code-block:: sql

    INSERT INTO entities_category
                (name)
    (SELECT Md5(Random() :: text) AS descr
     FROM   generate_series(1, 1000000));

You don't need to understand the full details of the sql above, it creates one million numbers and :code:`md5-s` them to generate the name, then inserts it in the DB.

Now, instead of sorting the whole table, you can get the max id,
generate a random number in range [1, max_id], and filter that. You are assuming that there have been no deletions.

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

If your models has deletions, you can sligthtly modify the functions, to loop until you get a valid :code:`Category`.

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

Unless your model has a lot of deletions, the :code:`while True:` loop return quickly. Lets use :code:`timeit` to see the differences.

.. code-block:: python

    In [14]: timeit.timeit(get_random3, number=100)
    Out[14]: 0.20055226399563253

    In [15]: timeit.timeit(get_random, number=100)
    Out[15]: 56.92513192095794

:code:`get_random3` is about 283 time faster than :code:`get_random`. :code:`get_random` is the most generic way, but the technique in :code:`get_random3` will work unless you change changed the default way Django generates the id - autoincrementing integers, or there have been too many deletions.


