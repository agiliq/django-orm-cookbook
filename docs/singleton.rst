특정 모델의 항목이 하나만 생성되도록 강제하는 방법이 있나요?
============================================================================

특정 모델의 항목이 단 하나만 생성되도록 강제하고 싶을 때가 있습니다. 프로그램의 환경 설정 기록, 공유 자원에 대한 잠금 제어 등을 예로 들 수 있습니다.

다음은 :code:`Origin` 이라는 모델을 싱글턴(단일개체)으로 만드는 기법입니다.

.. code-block:: python

    class Origin(models.Model):
        name = models.CharField(max_length=100)

        def save(self, *args, **kwargs):
            if self.__class__.objects.count():
                self.pk = self.__class__.objects.first().pk
            super().save(*args, **kwargs)

위 코드는 :code:`save` 메서드를 재정의하여 :code:`pk` 필드를 이미 존재하는 값으로 지정하도록 강제합니다. 이로써 객체가 이미 존재할 때 :code:`create` 메서드를 호출하는 경우 :code:`IntegrityError` 예외가 발생하도록 합니다.
