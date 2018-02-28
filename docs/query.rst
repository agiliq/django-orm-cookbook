How to find the query associated with a queryset?
++++++++++++++++++++++++++++++++++++++++++++++++++

We have been working with Django ORM from long time, but deep inside us sometimes comes a thought how is django ORM making our queries execute or what is the SQL of the code which we are writing.

We have a model called events for querying it with django we will write something like ::

    >>> queryset = events.objects.all()
    >>> print(queryset.query)
    SELECT "events_event"."id", "events_event"."epic_id", "events_event"."details", "events_event"."years_ago" FROM "events_event"

.. image:: sql_query.png

Example 2 ::

    >>> queryset = Event.objects.filter(id=1, years_ago__gt=5)
    >>> print(queryset.query)
    SELECT "events_event"."id", "events_event"."epic_id", "events_event"."details", "events_event"."years_ago" FROM "events_event" WHERE ("events_event"."years_ago" > 5 AND "events_event"."id" = 1)
