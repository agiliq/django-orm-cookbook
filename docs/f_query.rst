How to filter a queryset with criteria based on comparing  their field values
==============================================================================

Django ORM makes it easy to filter based on fixed values.
To get all :code:`User` objects with :code:`first_name` starting with :code`'R'`,
you can do :code:`User.objects.filter(name_startswith='R')`.

What if you want to compare the first_name and last name?
You can use the :code:`F` object.


