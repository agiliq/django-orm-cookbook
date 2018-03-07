How to convert existing databases to Django models?
=====================================================

Django comes with a utility called inspectdb that can create models by introspecting an existing database. You can view the output by running this command ::

    $ python manage.py inspectdb

Befor running this you will have to configure youre database in the :code: `settings.py` file. The returned result will be a file having all model related stuff. You may want to save that file ::

    $ python manage.py inspectdb > models.py

The output file will be saved to your current directory.
