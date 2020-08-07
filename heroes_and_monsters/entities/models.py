from django.db import models

from django.conf import settings
from django.db import connection
from django.db.models import F


class Category(models.Model):
    name = models.CharField(max_length=100)

    hero_count = models.PositiveIntegerField()
    villain_count = models.PositiveIntegerField()

    class Meta:
        verbose_name_plural = "Categories"

    @classmethod
    def truncate(cls):
        with connection.cursor() as cursor:
            cursor.execute('DELETE FROM "{0}"'.format(cls._meta.db_table))

    def __str__(self):
        return self.name


from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType

# ...


class FlexCategory(models.Model):
    name = models.SlugField()
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey("content_type", "object_id")


class Origin(models.Model):
    name = models.CharField(max_length=100)

    def save(self, *args, **kwargs):
        if self.__class__.objects.count():
            self.pk = self.__class__.objects.first().pk
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Entity(models.Model):
    GENDER_MALE = "Male"
    GENDER_FEMALE = "Female"
    GENDER_OTHERS = "Others/Unknown"

    name = models.CharField(max_length=100)
    alternative_name = models.CharField(max_length=100, null=True, blank=True)

    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    flex_category = GenericRelation(FlexCategory, related_query_name="flex_category")
    origin = models.ForeignKey(Origin, on_delete=models.CASCADE)
    gender = models.CharField(
        max_length=100,
        choices=(
            (GENDER_MALE, GENDER_MALE),
            (GENDER_FEMALE, GENDER_FEMALE),
            (GENDER_OTHERS, GENDER_OTHERS),
        ),
    )
    description = models.TextField()

    added_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL
    )
    added_on = models.DateField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        abstract = True


class Hero(Entity):
    class Meta:
        verbose_name_plural = "Heroes"

    # def save(self, *args, **kwargs):
    #     super().save(*args, **kwargs)
    #     Category.objects.filter(pk=self.category_id).update(hero_count=F('hero_count')+1)

    is_immortal = models.BooleanField(default=True)

    benevolence_factor = models.PositiveSmallIntegerField(
        help_text="How benevolent this hero is?", default=50
    )
    arbitrariness_factor = models.PositiveSmallIntegerField(
        help_text="How arbitrary this hero is?", default=50
    )

    headshot = models.ImageField(null=True, blank=True, upload_to="hero_headshots/")

    # relationships
    father = models.ForeignKey(
        "self",
        related_name="children",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )
    mother = models.ForeignKey(
        "self", related_name="+", null=True, blank=True, on_delete=models.SET_NULL
    )
    spouse = models.ForeignKey(
        "self", related_name="+", null=True, blank=True, on_delete=models.SET_NULL
    )

    def save(self, *args, **kwargs):
        if not self.pk:
            Category.objects.filter(pk=self.category_id).update(
                hero_count=F("hero_count") + 1
            )
        super().save(*args, **kwargs)


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

    def save(self, *args, **kwargs):
        if not self.pk:
            Category.objects.filter(pk=self.category_id).update(
                villain_count=F("villain_count") + 1
            )
        super().save(*args, **kwargs)


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


# from django.db.models.signals import pre_save
# from django.dispatch import receiver

# @receiver(pre_save, sender=Hero, dispatch_uid="update_hero_count")
# def update_hero_count(sender, **kwargs):
#     hero = kwargs['instance']
#     if hero.pk:
#         Category.objects.filter(pk=hero.category_id).update(hero_count=F('hero_count')+1)

# @receiver(pre_save, sender=Villain, dispatch_uid="update_villain_count")
# def update_villain_count(sender, **kwargs):
#     villain = kwargs['instance']
#     if villain.pk:
#         Category.objects.filter(pk=villain.category_id).update(villain_count=F('villain_count')+1)
