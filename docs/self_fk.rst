How to include a self-referencing ForeignKey in a model
모델에 자기 참조 외래키를 어떻게 포함하는가?
========================================================================

| 자신을 참조하는 외래키는 중첩 또는 재귀 관계 모델에 사용합니다.
| 일대다 관계가 작동하는 것과 유사하지만 이름에서 알 수 있듯 모델은 자기 자신을 참조합니다.

자기 참조 외래키는 두 가지 방법으로 작성할 수 있습니다.

.. code-block:: python

    class Employee(models.Model):
        manager = models.ForeignKey('self', on_delete=models.CASCADE)

    # OR

    class Employee(models.Model):
        manager = models.ForeignKey("app.Employee", on_delete=models.CASCADE)
