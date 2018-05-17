How to update denormalized fields in other models on save?
========================================================================

You have models like this.

.. code-block:: python

    class Category(models.Model):
        name = models.CharField(max_length=100)
        hero_count = models.PositiveIntegerField()
        villain_count = models.PositiveIntegerField()

        class Meta:
            verbose_name_plural = "Categories"


    class Hero(models.Model):
        name = models.CharField(max_length=100)
        category = models.ForeignKey(Category, on_delete=models.CASCADE)
        # ...


    class Villain(models.Model):
        name = models.CharField(max_length=100)
        category = models.ForeignKey(Category, on_delete=models.CASCADE)
        # ...


You need the :code:`hero_count` and :code:`villain_count`, to be updated when new objects are created.

You can do something like this

.. code-block:: python

    class Hero(models.Model):
        # ...

        def save(self, *args, **kwargs):
            if not self.pk:
                Category.objects.filter(pk=self.category_id).update(hero_count=F('hero_count')+1)
            super().save(*args, **kwargs)


    class Villain(models.Model):
        # ...

        def save(self, *args, **kwargs):
            if not self.pk:
                Category.objects.filter(pk=self.category_id).update(villain_count=F('villain_count')+1)
            super().save(*args, **kwargs)


Note how we did not use :code:`self.category.hero_count += 1`, as :code:`update` will do a DB update.

The alternative method is using `signals`. You can do it like this.

.. code-block:: python

    from django.db.models.signals import pre_save
    from django.dispatch import receiver

    @receiver(pre_save, sender=Hero, dispatch_uid="update_hero_count")
    def update_hero_count(sender, **kwargs):
        hero = kwargs['instance']
        if hero.pk:
            Category.objects.filter(pk=hero.category_id).update(hero_count=F('hero_count')+1)

    @receiver(pre_save, sender=Villain, dispatch_uid="update_villain_count")
    def update_villain_count(sender, **kwargs):
        villain = kwargs['instance']
        if villain.pk:
            Category.objects.filter(pk=villain.category_id).update(villain_count=F('villain_count')+1)


Signals vs Overriding :code:`.save`
++++++++++++++++++++++++++++++++++++


Since either of signals of :code:`.save` can be used for the save behviour, when should you use which one? I follow a simple rule.

- If your fields depend on a model you control, override :code:`.save`
- If your fields depend on a model from a 3rd party app, which you do no control, use signals.

