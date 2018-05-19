How to include a self-referencing ForeignKey in a model
========================================================================

Self-referencing foreign keys are used to model nested relationships or recursive relationships. They work similar to how One to Many relationships. But as the name suggests, the model references itself.

Self reference Foreignkey can be achived in two ways.

.. code-block:: python


    class Employee(models.Model):
        manager = models.ForeignKey('self', on_delete=models.CASCADE)

    # OR

    class Employee(models.Model):
        manager = models.ForeignKey("app.Employee", on_delete=models.CASCADE)

