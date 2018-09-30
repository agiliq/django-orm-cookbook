기본 키(PK)로 ID 대신 UUID를 사용할 수 있나요?
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

장고에서 모델을 생성하면 ID 필드가 기본 키로 생성됩니다. ID 필드의 기본 데이터 유형은 양의 정수입니다.

양의 정수가 아니라 UUID를 기본 키로 사용하고 싶다면 장고 1.8 버전에서 추가된 :code:`UUIDField` 를 사용하면 됩니다. ::

    import uuid
    from django.db import models

    class Event(models.Model):
        id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
        details = models.TextField()
        years_ago = models.PositiveIntegerField()

    >>> eventobject = Event.objects.all()
    >>> eventobject.first().id
    '3cd2b4b0c36f43488a93b3bb72029f46'