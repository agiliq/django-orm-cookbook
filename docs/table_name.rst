모델에 연결된 표의 이름을 지정할 수 있나요?
=========================================================================

여러분이 모델에 연결된 데이터베이스 표의 이름을 직접 지정하지 않으면 장고가 자동으로 표의 이름을 지어 줍니다. 자동으로 붙는 데이터베이스 표의 이름은 "앱의 레이블"(manage.py startapp 명령에서 지은 이름)과 모델 클래스의 이름을 밑줄 기호로 연결한 것이 됩니다.

이 책의 예제에서는 :code:`entities` 앱과 :code:`events` 앱을 사용했으므로 모든 모델의 표 이름이 :code:`entities_` 또는 :code:`events_`로 시작합니다.

.. image:: db_table.png

이 이름을 직접 붙이시려면 모델의 :code:`Meta` 클래스에 :code:`db_table` 값을 설정하면 됩니다. ::

    class TempUser(models.Model):
        first_name = models.CharField(max_length=100)
        . . .
        class Meta:
            db_table = "temp_user"