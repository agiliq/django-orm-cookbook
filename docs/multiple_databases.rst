장고 프로젝트 하나에서 여러 개의 데이터베이스를 사용할 수 있나요?
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

데이터베이스의 접속에 관련된 설정은 대부분 :code:`settings.py` 파일에서 이루어집니다. 장고 프로젝트에 여러 개의 데이터베이스를 추가하려면 해당 파일의 :code:`DATABASES` 사전에 등록하면 됩니다. ::

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

여러 개의 데이터베이스를 함께 사용하려면 데이터베이스 중계기(database router)에 대해 알아야 합니다. 장고의 기본 중계 설정은 데이터베이스를 특정하지 않은 경우 기본(default) 데이터베이스로 중계하는 것입니다. :code:`DATABASE_ROUTERS` 설정의 기본값은 :code:`[]` 입니다. 중계기는 다음과 같이 정의할 수 있습니다. ::

    class DemoRouter:
        """
        user_data 앱의 모델에서 수행되는 모든 데이터베이스 연산을 제어하는 중계기
        """
        def db_for_read(self, model, **hints):
            """
            user_data 앱의 모델을 조회하는 경우 users_db로 중계한다.
            """
            if model._meta.app_label == 'user_data':
                return 'users_db'
            return None

        def db_for_write(self, model, **hints):
            """
            user_data 앱의 모델을 기록하는 경우 users_db로 중계한다.
            """
            if model._meta.app_label == 'user_data':
                return 'users_db'
            return None

        def allow_relation(self, obj1, obj2, **hints):
            """
            user_data 앱의 모델과 관련된 관계 접근을 허용한다.
            """
            if obj1._meta.app_label == 'user_data' or \
               obj2._meta.app_label == 'user_data':
               return True
            return None

        def allow_migrate(self, db, app_label, model_name=None, **hints):
            """
            user_data 앱의 모델에 대응하는 표가 users_db 데이터베이스에만 생성되도록 한다.
            """
            if app_label == 'user_data':
                return db == 'users_db'
            return None


중계기를 위와 같이 설정해 두었으면, 모델이 서로 다른 데이터베이스를 사용하도록 다음과 같이 정의할 수 있습니다. ::

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

여러 개의 데이터베이스를 관리할 때 사용하는 마이그레이션 명령도 알아두세요. ::

        $ ./manage.py migrate --database=users_db
