### 장고 ORM 요리책

(렌더링 된 문서: https://django-orm-cookbook-ko.readthedocs.io/en/latest/)


장고 ORM 요리책은 장고를 이용한 다양한 레시피(조리법)를 담은 책입니다. `장고 ORM/쿼리셋으로 ~을 하려면 어떻게 하나요?` 하는 50여 개의 질문과 답을 담고 있습니다.

이 책에서는 전체 주제 공통으로 아래에서 설명하는 데이터 모델을 이용합니다.


### 실습용 모델 준비

여러분은 장고를 이용하여 UMSRA의 연구원들이 사용할 모델과 관리자 뷰(admin)를 제작하는 중입니다. 여러분은 프로젝트를 개체를 나타내는 `entities` 앱과 사건을 나타내는 `events` 앱 두 개로 나누어 작성하게 되었습니다. 그리고 각 앱의 모델을 다음과 같이 준비했습니다. (지금 자세히 보지 않아도 됩니다. 책을 보다가 필요할 때 참고해주세요.)


#### Events 앱의 모델


    from django.db import models
    from django.utils.text import slugify
    from entities.models import Hero, Villain
    from django.contrib.auth.models import User
    import uuid
    
    class Epic(models.Model):
        name = models.CharField(max_length=255)
        participating_heroes = models.ManyToManyField(Hero)
        participating_villains = models.ManyToManyField(Villain)
    
    
    class Event(models.Model):
        id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
        epic = models.ForeignKey(Epic, on_delete=models.CASCADE)
        details = models.TextField()
        years_ago = models.PositiveIntegerField()
    
    
    class EventHero(models.Model):
        event = models.ForeignKey(Event, on_delete=models.CASCADE)
        hero = models.ForeignKey(Hero, on_delete=models.CASCADE)
        is_primary = models.BooleanField()
    
    
    class EventVillain(models.Model):
        event = models.ForeignKey(Event, on_delete=models.CASCADE)
        hero = models.ForeignKey(Villain, on_delete=models.CASCADE)
        is_primary = models.BooleanField()
    
    
    class UserParent(models.Model):
        user = models.OneToOneField(
            User,
            on_delete=models.CASCADE,
            primary_key=True,
        )
        father_name = models.CharField(max_length=100)
        mother_name = models.CharField(max_length=100)
    
    class Article(models.Model):
        headline = models.CharField(max_length=100)
        pub_date = models.DateField()
        reporter = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reporter')
        slug = models.SlugField()
    
        def save(self, *args, **kwargs):
            self.slug = slugify(self.headline)
            super(Article, self).save(*args, **kwargs)
        def __str__(self):
            return self.headline
    
        class Meta:
            ordering = ('headline',)
    
    class TempUser(models.Model):
        first_name = models.CharField(max_length=100)
    
        class Meta:
            managed = False
            db_table = "temp_user"


    class ColumnName(models.Model):
        a = models.CharField(max_length=40,db_column='column1')
        column2 = models.CharField(max_length=50)
    
        def __str__(self):
            return self.a


#### Entities 앱의 모델

    from django.db import models

    from django.conf import settings
    
    
    class Category(models.Model):
        name = models.CharField(max_length=100)
    
        class Meta:
            verbose_name_plural = "Categories"
    
        def __str__(self):
            return self.name
    
    
    class Origin(models.Model):
        name = models.CharField(max_length=100)
    
        def __str__(self):
            return self.name
    
    
    class Entity(models.Model):
        GENDER_MALE = "Male"
        GENDER_FEMALE = "Female"
        GENDER_OTHERS = "Others/Unknown"
    
        name = models.CharField(max_length=100)
        alternative_name = models.CharField(
            max_length=100, null=True, blank=True
        )
    
    
        category = models.ForeignKey(Category, on_delete=models.CASCADE)
        origin = models.ForeignKey(Origin, on_delete=models.CASCADE)
        gender = models.CharField(
            max_length=100,
            choices=(
                (GENDER_MALE, GENDER_MALE),
                (GENDER_FEMALE, GENDER_FEMALE),
                (GENDER_OTHERS, GENDER_OTHERS),
            )
        )
        description = models.TextField()
    
        added_by = models.ForeignKey(settings.AUTH_USER_MODEL,
            null=True, blank=True, on_delete=models.SET_NULL)
        added_on = models.DateField(auto_now=True)
    
        def __str__(self):
            return self.name
    
        class Meta:
            abstract = True
    
    
    class Hero(Entity):
    
        class Meta:
            verbose_name_plural = "Heroes"
    
        is_immortal = models.BooleanField(default=True)
    
        benevolence_factor = models.PositiveSmallIntegerField(
            help_text="How benevolent this hero is?"
        )
        arbitrariness_factor = models.PositiveSmallIntegerField(
            help_text="How arbitrary this hero is?"
        )
    
        headshot = models.ImageField(null=True, blank=True, upload_to="hero_headshots/")
    
        # relationships
        father = models.ForeignKey(
            "self", related_name="children", null=True, blank=True, on_delete=models.SET_NULL
        )
        mother = models.ForeignKey(
            "self", related_name="+", null=True, blank=True, on_delete=models.SET_NULL
        )
        spouse = models.ForeignKey(
            "self", related_name="+", null=True, blank=True, on_delete=models.SET_NULL
        )
    
    
    class HeroProxy(Hero):
    
        class Meta:
            proxy = True
    
    class Villain(Entity):
        is_immortal = models.BooleanField(default=False)
    
        malevolence_factor = models.PositiveSmallIntegerField(
            help_text="How malevolent this villain is?"
        )
        power_factor = models.PositiveSmallIntegerField(
            help_text="How powerful this villain is?"
        )
        is_unique = models.BooleanField(default=True)
        count = models.PositiveSmallIntegerField(default=1)
    
    
    class HeroAcquaintance(models.Model):
        "Non family contacts of a Hero"
        hero = models.OneToOneField(Hero, on_delete=models.CASCADE)
    
        friends = models.ManyToManyField(Hero, related_name="+")
        detractors = models.ManyToManyField(Hero, related_name="+")
        main_anatagonists = models.ManyToManyField(Villain, related_name="+")
    
    
    class AllEntity(models.Model):
        name = models.CharField(max_length=100)
    
        class Meta:
            managed = False
            db_table = "entities_entity"
