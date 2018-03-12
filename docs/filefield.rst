How to filter FileField without any file?
++++++++++++++++++++++++++++++++++++++++++++++

Any :code:`FileField` or :code:`ImageField` mostly stores the path of the image wherever they are stored. So at sometimes when images/files are not stored the :code:`Field` will be left blank as a empty string. So to query FileField without any file we can query as under. ::

    no_files_objects = MyModel.objects.filter(file='') // This query will return all the objects of the model which don't have file stored in them.