어떤 종류의 객체와도 연관 지을 수 있는 Generic 모델을 만드는 방법은? (예: 카테고리 또는 코멘트)
=============================================================================================================

다음과 같은 모델이 있습니다.

.. code-block:: python

    class Category(models.Model):
        name = models.CharField(max_length=100)
        # ...

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


| ``Category`` 는 일반적인 모델입니다. 당신은 아마도 여러 모델 클래스 오브젝트에 카테고리를 적용하고 싶을 것입니다.
| 그렇다면 다음과 같이 할 수 있습니다.


.. code-block:: python

    from django.contrib.contenttypes.fields import GenericForeignKey
    from django.contrib.contenttypes.models import ContentType
    # ...

    class FlexCategory(models.Model):
        name = models.SlugField()
        content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
        object_id = models.PositiveIntegerField()
        content_object = GenericForeignKey('content_type', 'object_id')


    class Hero(models.Model):
        name = models.CharField(max_length=100)
        flex_category = GenericRelation(FlexCategory, related_query_name='flex_category')
        # ...


    class Villain(models.Model):
        name = models.CharField(max_length=100)
        flex_category = GenericRelation(FlexCategory, related_query_name='flex_category')
        # ...

| ``FlexCategory`` 에 ``ForeignKey`` 와 ``PositiveIntegerField`` 를 사용하여 ``GenericForeignKey`` 필드를 적용했습니다.
| 그리고 카테고리를 적용하려는 모델에 ``GenericRelation`` 을 추가했습니다.
|
| 데이터베이스 레벨에서 보면 다음과 같습니다.


================== ======================= ====================================================================
 Column             Type                    Modifiers
================== ======================= ====================================================================
 id                 integer                 not null default nextval('entities_flexcategory_id_seq'::regclass)
 name               character varying(50)   not null
 object_id          integer                 not null
 content_type_id    integer                 not null
================== ======================= ====================================================================

``Hero`` 는 다음과 같이 카테고리를 생성할 수 있습니다.

.. code-block:: python

    hero = Hero.objects.create(name='Hades')
    FlexCategory.objects.create(content_object=hero, name="mythic")

'ghost'로 분류된 ``Hero`` 는 다음과 같이 얻을 수 있습니다.

.. code-block:: python

    Hero.objects.filter(flex_category__name='ghost')

위의 쿼리는 다음과 같은 sql을 만듭니다.

.. code-block:: sql

    SELECT "entities_hero"."name"
    FROM "entities_hero"
    INNER JOIN "entities_flexcategory" ON ("entities_hero"."id" = "entities_flexcategory"."object_id"
                                           AND ("entities_flexcategory"."content_type_id" = 8))
    WHERE "entities_flexcategory"."name" = ghost
