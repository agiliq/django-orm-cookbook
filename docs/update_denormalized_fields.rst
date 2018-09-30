모델 인스턴스를 저장할 때, 다른 모델에 반정규화된 필드를 함께 갱신하는 방법이 있나요?
==========================================================================================================

모델을 다음과 같이 구성했다고 합시다.

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


Hero 모델과 Villain 모델의 항목을 새로 저장할 때, Category 모델의 :code:`hero_count` 필드와 :code:`villain_count` 필드를 갱신해야 합니다.

다음과 같이 Hero 모델과 Villain 모델의 :code:`save` 메서드를 재정의하면 됩니다.

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


위 코드에서 :code:`self.category.hero_count += 1`과 같이 인스턴스의 값을 수정하는 것이 아니라, :code:`update` 메서드로 데이터베이스의 갱신을 수행하도록 한 것을 확인하시기 바랍니다.

또 다른 방법으로, '시그널'이라는 기능을 이용하는 방법이 있습니다. 시그널을 이용하는 예를 살펴봅시다.

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


:code:`save` 메서드 재정의 방법과 시그널의 비교
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

:code:`save` 메서드를 재정의하는 방법과 시그널을 이용하는 방법 모두 사용할 수 있습니다. 어느 것을 사용하는 것이 좋을까요? 다음 규칙을 권해 드립니다.

- 반정규화 필드에 영향을 끼치는 모델을 여러분이 통제할 수 있다면 `save` 메서드를 재정의합니다.
- 반정규화 필드에 영향을 끼치는 모델을 여러분이 통제할 수 없다면(그 영향이 라이브러리 등에서 이루어진다면) 시그널을 이용합니다.

