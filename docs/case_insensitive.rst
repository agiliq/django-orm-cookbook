쿼리셋을 어떻게 대소문자 관계없이 정렬할 수 있을까요?
============================================================

.. image:: usertable2.png

어떤 문자열들을 :code:`order_by` 를 통해 정렬하려고 할때, 정렬은 알파벳 순서 그리고 알파벳 대소문자를 구분합니다. 예를 들면 다음과 같습니다.

.. code-block:: ipython

    >>> User.objects.all().order_by('username').values_list('username', flat=True)
    <QuerySet ['Billy', 'John', 'Radha', 'Raghu', 'Ricky', 'Ritesh', 'johny', 'johny1', 'paul', 'rishab', 'sharukh', 'sohan', 'yash']>

만약 쿼리셋을 대소문자 구분 없이 문자열을 정렬하고 싶다면 다음과 같이 할 수 있습니다.

.. code-block:: ipython

    >>> from django.db.models.functions import Lower
    >>> User.objects.all().order_by(Lower('username')).values_list('username', flat=True)
    <QuerySet ['Billy', 'John', 'johny', 'johny1', 'paul', 'Radha', 'Raghu', 'Ricky', 'rishab', 'Ritesh', 'sharukh', 'sohan', 'yash']>

또 다른 방법으로는, :code:`Lower` 를 사용하여 Annotate된 필드를 생성하고, 해당 필드를 가지고 정렬 할 수 있습니다.

.. code-block:: python

    User.objects.annotate(
        lower_name=Lower('username')
    ).order_by('lower_name').values_list('username', flat=True)
