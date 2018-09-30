:code:`null=True` 와 :code:`blank=True` 의 차이가 무엇인가요?
====================================================================================================

:code:`null` 과 :code:`blank` 는 둘 다 기본값이 :code:`False` 입니다. 이 두 설정은 모두 필드(열) 수준에서 동작합니다. 즉, 필드(열)를 비워두는 것을 허용할 것인지를 설정합니다.

:code:`null=True` 는 필드의 값이 NULL(정보 없음)로 저장되는 것을 허용합니다. 결국 데이터베이스 열에 관한 설정입니다. ::

    date = models.DateTimeField(null=True)

:code:`blank=True` 는 필드가 폼(입력 양식)에서 빈 채로 저장되는 것을 허용합니다. 장고 관리자(admin) 및 직접 정의한 폼에도 반영됩니다. ::

    title = models.CharField(blank=True)  # 폼에서 비워둘 수 있음. 데이터베이스에는 ''이 저장됨.

:code:`null=True` 와 :code:`blank=True` 를 모두 지정하면 어떤 조건으로든 값을 비워둘 수 있음을 의미합니다. ::

    epic = models.ForeignKey(null=True, blank=True)
    # 단, CharFields()와 TextFields()에서는 예외입니다.
    # 장고는 이 경우 NULL을 저장하지 않으며, 빈 값을 빈 문자열('')로 저장합니다.

또 하나 예외적인 경우가 있습니다. 불리언 필드(:code:`BooleanField`)에 NULL을 입력할 수 있도록 하려면 :code:`null=True` 를 설정하는 것이 아니라, 널 불리언 필드(:code:`NullBooleanField`)를 사용해야 합니다.