How to find second largest record using Django ORM ?
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

We have come across situations when we want to query second highest user depending on his age or salary. Though ORM gives as the flexibility of finding first(), last() item from the queryset but not nth item.

.. image:: usertable.png

We can find Nth records from the query by using slice operator.

    >>> u = User.objects.order_by('-id')[1] // Second Highest record w.r.t 'id'
    >>> u.first_name
    'Raghu'
    >>> u = User.objects.order_by('-id')[2] // Third Highest record w.r.t 'id'
    >>> u.first_name
    'Sohan'
