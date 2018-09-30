모델에 자기 참조 외래 키를 정의할 수 있나요?
========================================================================

자기 참조 외래 키를 이용하여 중첩 관계·재귀 관계를 표현할 수 있습니다. 일대다 관계와 유사하지만, 이름에서 알 수 있듯이 모델이 자기 자신을 참조한다는 특징이 있습니다.

자기 참조 외래 키는 아래의 두 가지 방법으로 작성할 수 있습니다.

.. code-block:: python

    class Employee(models.Model):
        manager = models.ForeignKey('self', on_delete=models.CASCADE)

    # 또는

    class Employee(models.Model):
        manager = models.ForeignKey("app.Employee", on_delete=models.CASCADE)
