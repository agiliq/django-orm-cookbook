How to ensure that only one object can be created?
========================================================================

Sometimes you want to ensure that only one record can be created for a model. This is commonly required as application configuration store, or as a locking mechanism to access shared resources.

Let us convert our :code:`Origin` model to be singleton.

.. code-block:: python

    class Origin(models.Model):
        name = models.CharField(max_length=100)

        def save(self, *args, **kwargs):
            if self.__class__.objects.count():
                self.pk = self.__class__.objects.first().pk
            super().save(*args, **kwargs)

What did we do? We overrode the :code:`save` method, and set the :code:`pk` to an existing value. This ensures that when :code:`create` is called and any object exists, an :code:`IntegrityError` is raised.
