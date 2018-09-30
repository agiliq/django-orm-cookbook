장고에서 서브쿼리 식을 사용할 수 있나요?
==============================================================

장고에서 SQL 서브쿼리(subquery, 질의문 내의 하위 질의) 식을 사용할 수 있습니다. 간단한 것부터 시작해 봅시다. :code:`auth_user` 모델과 일 대 일(:code:`OneToOne`) 관계로 연결된 :code:`UserParent` 모델이 있다고 합시다. 아래 코드로 :code:`UserParent` 모델에서 :code:`auth_user`를 가진 행을 모두 구할 수 있습니다.

.. code-block:: ipython

    >>> from django.db.models import Subquery
    >>> users = User.objects.all()
    >>> UserParent.objects.filter(user_id__in=Subquery(users.values('id')))
    <QuerySet [<UserParent: UserParent object (2)>, <UserParent: UserParent object (5)>, <UserParent: UserParent object (8)>]>

조금 더 까다로운 예제를 살펴봅시다. :code:`Category` 모델의 각 행 별로, 가장 선한 :code:`Hero` 행을 구해 봅시다.

모델은 다음과 같이 준비합니다.

.. code-block:: python

    class Category(models.Model):
        name = models.CharField(max_length=100)


    class Hero(models.Model):
        # ...
        name = models.CharField(max_length=100)
        category = models.ForeignKey(Category, on_delete=models.CASCADE)

        benevolence_factor = models.PositiveSmallIntegerField(
            help_text="How benevolent this hero is?",
            default=50
        )


이 모델에서 가장 선한 영웅을 구하려면 다음 코드를 실행합니다.

.. code-block:: python

    hero_qs = Hero.objects.filter(
        category=OuterRef("pk")
    ).order_by("-benevolence_factor")
    Category.objects.all().annotate(
        most_benevolent_hero=Subquery(
            hero_qs.values('name')[:1]
        )
    )

이 코드가 실행하는 SQL 질의문은 다음과 같습니다.

.. code-block:: sql

    SELECT "entities_category"."id",
           "entities_category"."name",

      (SELECT U0."name"
       FROM "entities_hero" U0
       WHERE U0."category_id" = ("entities_category"."id")
       ORDER BY U0."benevolence_factor" DESC
       LIMIT 1) AS "most_benevolent_hero"
    FROM "entities_category"


질의문을 한 단계씩 나누어 살펴봅시다. 다음 코드가 첫 번쨰 단계입니다.

.. code-block:: python

    hero_qs = Hero.objects.filter(
        category=OuterRef("pk")
    ).order_by("-benevolence_factor")

:code:`Hero`의 행들을 선함(:code:`benevolence_factor`)에 따라 내림차순(DESC)으로 정렬하여 선택합니다. 그리고 :code:`category=OuterRef("pk")`를 이용해 이 선택이 서브쿼리로 사용될 수 있도록 준비합니다.


그 뒤 :code:`most_benevolent_hero=Subquery(hero_qs.values('name')[:1])`로 서브쿼리에 별칭을 붙여 :code:`Category` 쿼리셋 안에서 사용합니다. 이 때, :code:`hero_qs.values('name')[:1]`는 서브쿼리에서 첫 번째 행의 name 필드를 구하는 코드입니다.

