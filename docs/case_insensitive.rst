How to order a queryset in case insensitive manner?
============================================================

.. image:: usertable2.png

Whenever we try to do :code:`order_by` with some string value, the ordering happens alphabetically and w.r.t case. Like

.. code-block:: ipython

    >>> User.objects.all().order_by('username').values_list('username', flat=True)
    <QuerySet ['Billy', 'John', 'Radha', 'Raghu', 'Ricky', 'Ritesh', 'johny', 'johny1', 'paul', 'rishab', 'sharukh', 'sohan', 'yash']>

If we want to order queryset in case insensitive manner, we can do like this.

.. code-block:: ipython

    >>> from django.db.models.functions import Lower
    >>> User.objects.all().order_by(Lower('username')).values_list('username', flat=True)
    <QuerySet ['Billy', 'John', 'johny', 'johny1', 'paul', 'Radha', 'Raghu', 'Ricky', 'rishab', 'Ritesh', 'sharukh', 'sohan', 'yash']>

Alternatively, you can annotate with :code:`Lower` and then order on annotated field.

.. code-block:: python

    User.objects.annotate(
        uname=Lower('username')
    ).order_by('uname').values_list('username', flat=True)
