일대일 관계는 어떻게 나타내나요?
===================================================

일대일 관계란 두 표에서 각 항목이 서로 다른 표의 항목 단 하나와 연결되는 관계입니다. 우리가 쉽게 이해할 수 있는 예를 들자면, 우리들 각자는 생부와 생모를 각각 하나씩만 가질 수 있습니다.

다음 예는 장고의 사용자 인증 모델에 :code:`UserParent` 모델을 일대일 관계로 연결해서 각 사용자마다 사용자의 부모를 기록할 수 있도록 합니다.

.. code-block:: python

    from django.contrib.auth.models import User

    class UserParent(models.Model):
        user = models.OneToOneField(
            User,
            on_delete=models.CASCADE,
            primary_key=True,
        )
        father_name = models.CharField(max_length=100)
        mother_name = models.CharField(max_length=100)

>>> u1 = User.objects.get(first_name='Ritesh', last_name='Deshmukh')
>>> u2 = User.objects.get(first_name='Sohan', last_name='Upadhyay')
>>> p1 = UserParent(user=u1, father_name='Vilasrao Deshmukh', mother_name='Vaishali Deshmukh')
>>> p1.save()
>>> p1.user.first_name
'Ritesh'
>>> p2 = UserParent(user=u2, father_name='Mr R S Upadhyay', mother_name='Mrs S K Upadhyay')
>>> p2.save()
>>> p2.user.last_name
'Upadhyay'

on_delete 메서드는 그 필드에 연결된 항목이 삭제될 때 그 항목을 가리키는 항목들을 어떻게 처리해야 할지 설정합니다. 예를 들어, :code:`on_delete=models.CASCADE`(하위 삭제)는 연결된 항목이 삭제될 때 해당 항목을 함께 삭제하도록 합니다. 따라서, 다음 코드를 실행하면

>>> u2.delete()

:code:`User` 모델의 항목(u2) 뿐 아니라 :code:`UserParent`의 항목(p2)도 함께 삭제됩니다.
