How to add multiple databases to the django application ?
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

The configuration of database related stuff is mostly done in :code:`settings.py` file. So to add multiple database to our django project we need add them in :code:`DATABASES` dictionary. ::

    DATABASE_ROUTERS = ['path.to.DemoRouter']
    DATABASE_APPS_MAPPING = {'user_data': 'users_db',
                            'customer_data':'customers_db'}

    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
        },
        'users_db': {
            'NAME': 'user_data',
            'ENGINE': 'django.db.backends.postgresql',
            'USER': 'postgres_user',
            'PASSWORD': 'password'
        },
        'customers_db': {
            'NAME': 'customer_data',
            'ENGINE': 'django.db.backends.mysql',
            'USER': 'mysql_cust',
            'PASSWORD': 'root'
        }
    }

With multiple databases it will be good to talk about :code:`Database Router`. The default routing scheme ensures that if a database isn’t specified, all queries fall back to the default database. :code:`Database Router` defaults to :code:`[]`. ::

    class DemoRouter:
        """
        A router to control all database operations on models in the
        user application.
        """
        def db_for_read(self, model, **hints):
            """
            Attempts to read user models go to users_db.
            """
            if model._meta.app_label == 'user_data':
                return 'users_db'
            return None

        def db_for_write(self, model, **hints):
            """
            Attempts to write user models go to users_db.
            """
            if model._meta.app_label == 'user_data':
                return 'users_db'
            return None

        def allow_relation(self, obj1, obj2, **hints):
            """
            Allow relations if a model in the user app is involved.
            """
            if obj1._meta.app_label == 'user_data' or \
               obj2._meta.app_label == 'user_data':
               return True
            return None

        def allow_migrate(self, db, app_label, model_name=None, **hints):
            """
            Make sure the auth app only appears in the 'users_db'
            database.
            """
            if app_label == 'user_data':
                return db == 'users_db'
            return None


Respective models would be modified as ::

    class User(models.Model):
        username = models.Charfield(ax_length=100)
        . . .
            class Meta:
            app_label = 'user_data'

    class Customer(models.Model):
        name = models.TextField(max_length=100)
        . . .
            class Meta:
            app_label = 'customer_data'

Few helpful commnds while working with multiple databases. ::

        $ ./manage.py migrate --database=users_db
