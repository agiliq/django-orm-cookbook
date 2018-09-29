어떻게 데이터베이스 뷰에 모델을 추가하는가?
===============================================

| 데이터베이스 뷰는 쿼리로 정의된 데이터베이스에서 검색 가능한 객체입니다.
| 비록 뷰가 데이터를 저장하지는 않지만, 어떤 것들은 "가상 테이블"이라 불리며 테이블처럼 쿼리를 할 수 있습니다.
| 뷰는 조인을 사용해 둘 혹은 그 이상의 테이블에서 데이터를 조합할 수 있으며, 정보의 하위 부분만 포함합니다.
| 이로 인해 복잡한 쿼리를 쉽게 추상화하거나 은닉할 수 있습니다.

우리의 SqliteStuio에는 26개의 테이블을 볼 수 있고 뷰는 없습니다.

.. image:: before_view.png

간단한 뷰를 만들어봅시다.

.. code-block:: sql

  create view temp_user as
  select id, first_name
  from auth_user;

뷰가 생성된 후, 우리는 26개의 테이블과 1개의 뷰를 확인할 수 있습니다.

.. image:: after_view.png

앱에서 ``managed = False`` , ``db_table="temp_user"`` 로 관련 모델을 생성할 수 있습니다.

.. code-block:: python

    class TempUser(models.Model):
        first_name = models.CharField(max_length=100)

        class Meta:
            managed = False
            db_table = "temp_user"

>>> # 테이블에 수행하는 것과 유사하게 새로 생성된 뷰에 쿼리를 할 수 있습니다.
>>> TempUser.objects.all().values()
<QuerySet [{'first_name': 'Yash', 'id': 1}, {'first_name': 'John', 'id': 2}, {'first_name': 'Ricky', 'id': 3}, {'first_name': 'Sharukh', 'id': 4}, {'first_name': 'Ritesh', 'id': 5}, {'first_name': 'Billy', 'id': 6}, {'first_name': 'Radha', 'id': 7}, {'first_name': 'Raghu', 'id': 9}, {'first_name': 'Rishabh', 'id': 10}, {'first_name': 'John', 'id': 11}, {'first_name': 'Paul', 'id': 12}, {'first_name': 'Johny', 'id': 13}, {'first_name': 'Alien', 'id': 14}]>
>>> # 뷰에 새로운 레코드를 삽입할 수는 없습니다.
>>> TempUser.objects.create(first_name='Radhika', id=15)
Traceback (most recent call last):
...
django.db.utils.OperationalError: cannot modify temp_user because it is a view

union 연산이 있는 뷰는 다음을 참고하세요 :
http://books.agiliq.com/projects/django-admin-cookbook/en/latest/database_view.html?highlight=view
