How to speed tests by reusing database between test runs?
================================================================

When we execute the command :code:`python manage.py test`, a new db is created everytime. This doesn't matter much if we don't have many migrations.

But when we have many migrations, it takes a long time to recreate the database between the test runs. To avoid such situations, we may reuse the old database.

You can prevent the test databases from being destroyed by adding the :code:`--keepdb` flag to the test command. This will preserve the test database between runs. If the database does not exist, it will first be created. If any migrations have been added since the last test run,
they will be applied in order to keep it up to date.

.. code-block::python

    $ python manage.py test --keepdb

