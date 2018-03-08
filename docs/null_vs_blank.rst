What is the difference between :code:`null=True` and :code:`blank=True`?
===============================================================================

The default value of both :code:`null` and :code:`blank` is :code:`False`. Both of these values work at field level i.e., whether we want to keep a field null or blank.

:code:`null=True` will set the field's value to NULL i.e., no data. It is basically for the databases column value. ::

    date = models.DateTimeField(null=True)

:code:`blank=True` determines whether the field will be required in forms. This includes the admin and your own custom forms. ::

    title = models.CharField(blank=True) // title can be kept blank. In the database ("") will be stored.

:code:`null=True` :code:`blank=True` This means that the field is optional in all circumstances. ::

    epic = models.ForeignKey(null=True, blank=True)
    // The exception is CharFields() and TextFields(), which in Django are never saved as NULL. Blank values are stored in the DB as an empty string ('').

Also there is a special case, when you need to accept NULL values for a :code:`BooleanField`, use :code:`NullBooleanField`.