How to add a model for a database view?
===============================================

A database view is a searchable object in a database that is defined by a query.  Though a view doesn’t store data, some refer to a views as “virtual tables,” you can query a view like you can a table.  A view can combine data from two or more table, using joins, and also just contain a subset of information.  This makes them convenient to abstract, or hide, complicated queries.

In our SqliteStuio we can see 26 tables and no views.

.. image:: before_view.png

Lets create a simple view. ::

        create view temp_user as
            select id, first_name from auth_user;

After the view is created, we can see 26 tables and 1 view.

.. image:: after_view.png

We can create its related model in our app, by :code:`managed = False` and :code:`db_table="temp_user"` ::

    class TempUser(models.Model):
        first_name = models.CharField(max_length=100)

        class Meta:
            managed = False
            db_table = "temp_user"

    // We can query the newly created view similar to what we do for any table.
    >>> TempUser.objects.all().values()
    <QuerySet [{'first_name': 'Yash', 'id': 1}, {'first_name': 'John', 'id': 2}, {'first_name': 'Ricky', 'id': 3}, {'first_name': 'Sharukh', 'id': 4}, {'first_name': 'Ritesh', 'id': 5}, {'first_name': 'Billy', 'id': 6}, {'first_name': 'Radha', 'id': 7}, {'first_name': 'Raghu', 'id': 9}, {'first_name': 'Rishabh', 'id': 10}, {'first_name': 'John', 'id': 11}, {'first_name': 'Paul', 'id': 12}, {'first_name': 'Johny', 'id': 13}, {'first_name': 'Alien', 'id': 14}]>
    // You cannot insert new reord in a view.
    >>> TempUser.objects.create(first_name='Radhika', id=15)
    Traceback (most recent call last):
    ...
    django.db.utils.OperationalError: cannot modify temp_user because it is a view

For view having union operation refer to :
http://books.agiliq.com/projects/django-admin-cookbook/en/latest/database_view.html?highlight=view
