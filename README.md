### Django ORM cookbook


Django ORM cookbook is a set of recipes of how to do things with Django.
They take the form of about 50 questions of the form
`How to do X with Django ORM/Queryset`.

We have a set of models which we use across the book for answering these questions.

### The models

You plan to write a set of models and an assoicated admin for UMSRA researchers. You come up with two apps `entities` and `events`. The models are


#### Events

```python
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
```

#### Entities

```python
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
```
