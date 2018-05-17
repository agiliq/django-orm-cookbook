What signals are raised by Django during object creation or update?
========================================================================

Django provides signals which allows hooking into a model objects creation and deletion lifecycle. The signals provided by Django are

- :code:`pre_init`
- :code:`post_init`
- :code:`pre_save`
- :code:`post_save`
- :code:`pre_delete`
- :code:`post_delete`


Among these, the most commonly used signals are :code:`pre_save` and :code:`post_save`. We will look into them in detail.

Signals vs overriding .save
-----------------------------------

Since signals can be used for similar effects as overriding :code:`.save`, which one to use is a frequent source of confusion. Here is when you should use which.

- If you want other people, eg. third party apps, to override or customize the object :code:`save` behaviour, you should raise your own signals
- If you are hooking into the :code:`save` behavior of an app you do not control, you should hook into the :code:`post_save` or :code:`pre_save`
- If you are customizing the save behaviour of apps you control, you should override :code:`save`.

Lets take an example of a :code:`UserToken` model. This a class used for providing authentication and should get created whenever a :code:`User` is created.

.. code-block:: python

    class UserToken(models.Model):
        token = models.CharField(max_length=64)

        # ...

