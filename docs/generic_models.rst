분류·댓글처럼 아무 모델이나 가리킬 수 있는 범용 모델을 정의할 수 있나요?
============================================================================================================

다음 모델을 봐 주세요.

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


여기서 :code:`Category` 모델은 범용 모델로 고쳐 정의할 수 있습니다. 다른 모델에도 분류를 적용하고 싶을 테니까요. 다음과 같이 수정하면 됩니다.

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

수정한 코드에서는 :code:`FlexCategory` 모델에 외래 키 필드(:code:`ForeignKey`) 하나와 양의 정수 필드(:code:`PositiveIntegerField`) 하나를 정의하여 범용 외래 키 필드(:code:`GenericForeignKey`)를 사용할 수 있도록 하였습니다. 그리고 분류를 이용할 모델에 범용 관계 필드(:code:`GenericRelation`)를 추가했습니다.

:code:`FlexCategory` 모델의 데이터베이스 스키마는 다음과 같이 정의됩니다.

.. code-block

         Column      |         Type          |                             Modifiers
    -----------------+-----------------------+--------------------------------------------------------------------
     id              | integer               | not null default nextval('entities_flexcategory_id_seq'::regclass)
     name            | character varying(50) | not null
     object_id       | integer               | not null
     content_type_id | integer               | not null


:code:`Hero` 모델의 항목을 분류할 때는 다음과 같이 합니다.

.. code-block:: python

    hero = Hero.objects.create(name='Hades')
    FlexCategory.objects.create(content_object=hero, name="mythic")

'ghost'로 분류된 :code:`Hero`를 구하려면 다음과 같이 조회합니다.

.. code-block:: python

    Hero.objects.filter(flex_category__name='ghost')

위의 ORM 코드가 생성하는 SQL 질의문은 아래와 같습니다.

.. code-block:: sql

    SELECT "entities_hero"."name"
    FROM "entities_hero"
    INNER JOIN "entities_flexcategory" ON ("entities_hero"."id" = "entities_flexcategory"."object_id"
                                           AND ("entities_flexcategory"."content_type_id" = 8))
    WHERE "entities_flexcategory"."name" = ghost
