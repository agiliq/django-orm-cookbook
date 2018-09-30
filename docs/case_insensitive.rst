대문자·소문자를 구별하지 않고 정렬하려면 어떻게 하나요?
============================================================

.. image:: usertable2.png

:code:`order_by` 메서드로 쿼리셋을 정렬할 때, 텍스트 필드를 기준으로 하면 알파벳의 대문자·소문자를 구분하여 정렬이 수행됩니다. 다음 예에서 보듯, 대문자에 소문자보다 높은 우선순위가 부여됩니다.

.. code-block:: ipython

    >>> User.objects.all().order_by('username').values_list('username', flat=True)
    <QuerySet ['Billy', 'John', 'Radha', 'Raghu', 'Ricky', 'Ritesh', 'johny', 'johny1', 'paul', 'rishab', 'sharukh', 'sohan', 'yash']>

텍스트 필드에서 대문자·소문자를 구별하지 않고 정렬하려면 다음과 같이 :code:`Lower` 를 사용하면 됩니다.

.. code-block:: ipython

    >>> from django.db.models.functions import Lower
    >>> User.objects.all().order_by(Lower('username')).values_list('username', flat=True)
    <QuerySet ['Billy', 'John', 'johny', 'johny1', 'paul', 'Radha', 'Raghu', 'Ricky', 'rishab', 'Ritesh', 'sharukh', 'sohan', 'yash']>

:code:`annotate` 메서드로 :code:`Lower` 를 적용한 열을 준비하고, 그 열을 기준으로 정렬하는 방법도 가능합니다.

.. code-block:: python

    User.objects.annotate(
        lower_name=Lower('username')
    ).order_by('lower_name').values_list('username', flat=True)
