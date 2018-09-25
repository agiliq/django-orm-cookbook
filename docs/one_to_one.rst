일대일 관계는 어떻게 모델링하는가?
===============================================

| 관계 테이블의 한 레코드에 상응하는 단 하나의 레코드가 있을때 일대일 관계가 발생합니다.
| 여기 우리가 잘 알고 있는 예시가 있습니다. 각 개인은 단 하나의 생물학적 부모 즉, 어머니와 아버지를 가질 수 있습니다.
| 우리는 사용자 인증 모델을 가지고 있으므로, 아래에 설명한 대로 새로운 UserParent 모델을 추가할 것입니다.

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

| on_delete 메서드는 Django에 삭제하려는 모델 인스턴스에 의존하는 모델 인스턴스를 어떻게 처리해야 할지 지시합니다. (예: ForeignKey 관계)
| on_delete=models.CASCADE는 계단식 삭제 즉, 종속모델까지 삭제하도록 Django에 지시합니다.

>>> u2.delete()

이것은 ``UserParent`` 의 관계 레코드까지 함께 삭제합니다.
