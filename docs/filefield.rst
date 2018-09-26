어떻게 파일이 없는 Object를 FileField로 필터링 하나요?
++++++++++++++++++++++++++++++++++++++++++++++

:code:`FileField` 나 :code:`ImageField` 는 파일이나 이미지의 경로를 저장합니다. Database 레벨에선 둘 모두 :code:`CharField` 로 같습니다. 아래의 쿼리로 파일이 없는 object를 찾을 수 있습니다.

.. code-block:: python

    no_files_objects = MyModel.objects.filter(
        Q(file='')|Q(file=None)
    )
