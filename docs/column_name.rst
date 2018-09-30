모델 필드의 데이터베이스 열 이름을 지정할 수 있나요?
=============================================================================

모델 필드가 가리키는 데이터베이스의 열 이름을 지정하려면 필드 인스턴스의 초기화 매개변수 :code:`db_column` 에 원하는 이름을 전달하면 됩니다. 이 매개변수에 인자를 전달하지 않으면 필드 이름과 동일한 이름이 사용됩니다. ::

    class ColumnName(models.Model):
        a = models.CharField(max_length=40,db_column='column1')
        column2 = models.CharField(max_length=50)

        def __str__(self):
            return self.a

.. image:: db_column.png

위 예에서 보듯, :code:`db_column` 으로 지정한 이름이 필드 이름보다 우선순위가 높습니다. 첫 번째 열의 이름이 a가 아니라 column1로 지어졌습니다.
