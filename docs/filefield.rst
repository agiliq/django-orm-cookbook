FileField에 파일이 들어있지 않은 행은 어떻게 구할 수 있나요?
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

장고의 :code:`FileField`와 :code:`ImageField`는 파일과 이미지 파일의 경로를 저장합니다. 이것은 응용 수준에서의 구별이고, 데이터베이스 수준에서는 모두 :code:`CharField`와 동일한 방식으로 저장됩니다. 파일이 없는 행을 구하려면 다음 코드를 실행하면 됩니다.

.. code-block:: python

    no_files_objects = MyModel.objects.filter(
        Q(file='')|Q(file=None)
    )
