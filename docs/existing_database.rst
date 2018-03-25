How to convert existing databases to Django models?
=====================================================

Django comes with a utility called :code:`inspectdb` that can create models by introspecting an existing database. You can view the output by running this command ::

    $ python manage.py inspectdb

Befor running this you will have to configure your database in the :code:`settings.py` file. The result will be a file containing a model for each table. You may want to save that file ::

    $ python manage.py inspectdb > models.py

The output file will be saved to your current directory. Move that file to the correct app and you have a good starting point for further customizations.
