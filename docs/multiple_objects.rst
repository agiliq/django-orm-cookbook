여러 개의 행을 한번에 생성하는 방법이 있나요?
+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

여러 개의 신규 객체를 한꺼번에 저장하고 싶은 경우가 있습니다. 예를 들어, 여러 개의 분류 항목을 단번에 생성하되, 데이터베이스에 질의를 여러 번 수행하지 않아야 한다고 합시다.
:code:`bulk_create` 메서드를 이용하면 여러 개의 신규 객체를 한 번에 저장할 수 있습니다.

다음 예를 살펴보세요.

.. code-block:: ipython

    >>> Category.objects.all().count()
    2
    >>> Category.objects.bulk_create(
        [Category(name="God"),
         Category(name="Demi God"),
         Category(name="Mortal")]
    )
    [<Category: God>, <Category: Demi God>, <Category: Mortal>]
    >>> Category.objects.all().count()
    5

:code:`bulk_create` 메서드는 저장되지 않은 객체들을 담은 리스트를 인자로 전달받습니다.
