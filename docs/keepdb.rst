How to speed tests by reusing database between test runs?
================================================================

Whenever we execute the command :code:`python manage.py test` new db is created everytime. This won't effect if we have less migrations to execute or db size is small.
But when we have many migrations,it takes long time to run the test cases. So to avoid such situations we may keep the old database for our use.
You can prevent the test databases from being destroyed by adding the :code:`--keepdb` flag to the test command. This will preserve the test database between runs. If the database does not exist, it will first be created.
Any migrations will also be applied in order to keep it up to date. ::

    $ python manage.py test --keepdb

