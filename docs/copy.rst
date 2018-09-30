기존에 저장된 행을 복사해 새로 저장하는 방법은 무엇인가요?
========================================================================

장고 ORM에는 모델 인스턴스를 복사하는 내장 메서드가 없습니다. 하지만 모든 필드의 값을 복사하여 새 인스턴스를 만들고 새로 저장하는 것은 어렵지 않습니다.

모델 인스턴스를 저장할 때, :code:`pk` 필드 값이 :code:`None` 으로 지정되어 있으면 데이터베이스에 새 행으로 저장됩니다. :code:`pk` 외의 모든 필드 값은 그대로 복제됩니다.

.. code-block:: ipython

    In [2]: Hero.objects.all().count()
    Out[2]: 4

    In [3]: hero = Hero.objects.first()

    In [4]: hero.pk = None

    In [5]: hero.save()

    In [6]: Hero.objects.all().count()
    Out[6]: 5


