from django.contrib.auth.models import User
from django.db.models import OuterRef, Subquery, F
from django.db.models.functions import Substr
from django.db.utils import IntegrityError
from django.test import TestCase

from events.tests import GlobalUserTestData
from .models import Hero, Category, Origin


class GlobalCategoryTestData:
    def setUp(self):
        self.bulk_create_category()

    def bulk_create_category(self):
        Category.objects.bulk_create(
            [
                Category(name="God", hero_count=0, villain_count=0),
                Category(name="Demi God", hero_count=0, villain_count=0),
                Category(name="Mortal", hero_count=0, villain_count=0),
            ]
        )


class TestSubQuery(GlobalCategoryTestData, TestCase):
    def setUp(self):
        super().setUp()
        Origin.objects.create(name="origin_1")
        Hero.objects.bulk_create(
            [
                Hero(
                    name="Zeus",
                    description="A greek God",
                    benevolence_factor=80,
                    category_id=2,
                    origin_id=1,
                ),
                Hero(
                    name="ZeuX",
                    description="A greek God",
                    benevolence_factor=80,
                    category_id=2,
                    origin_id=1,
                ),
                Hero(
                    name="Xeus",
                    description="A greek God",
                    benevolence_factor=80,
                    category_id=2,
                    origin_id=1,
                ),
                Hero(
                    name="Poseidon",
                    description="A greek God",
                    benevolence_factor=80,
                    category_id=2,
                    origin_id=1,
                ),
            ]
        )

    def test_sub_query(self):
        hero_qs = Hero.objects.filter(category=OuterRef("pk")).order_by(
            "-benevolence_factor"
        )

        cateogories = Category.objects.all().annotate(
            most_benevolent_hero=Subquery(hero_qs.values("name")[:1])
        )
        output_category = ["God", "Demi God", "Mortal"]
        self.assertEqual(
            list(cateogories.values_list("name", flat=True)), output_category
        )


class TestFQuery(TestCase):
    def setUp(self):
        User.objects.create_user(
            email="shabda@example.com",
            username="shabda",
            first_name="Shabda",
            last_name="Raaj",
        )
        User.objects.create_user(
            email="guido@example.com",
            username="Guido",
            first_name="Guido",
            last_name="Guido",
        )

    def test_simple_f_expression(self):
        users = User.objects.filter(last_name=F("first_name"))
        output_user = ["Guido"]
        self.assertEqual(list(users.values_list("first_name", flat=True)), output_user)

    def test_annotate_f_expression_with_substr(self):
        User.objects.create_user(
            email="guido@example.com",
            username="Tim",
            first_name="Tim",
            last_name="Teters",
        )
        users = User.objects.annotate(
            first=Substr("first_name", 1, 1), last=Substr("last_name", 1, 1)
        ).filter(first=F("last"))
        output_user = ["Guido", "Tim"]
        self.assertEqual(list(users.values_list("first_name", flat=True)), output_user)


class TestBulkCreate(GlobalCategoryTestData, TestCase):
    def setUp(self):
        pass

    def test_bulk_create(self):
        category_count = Category.objects.all().count()
        self.assertEqual(category_count, 0)

        self.bulk_create_category()

        category_count = Category.objects.all().count()
        self.assertEqual(category_count, 3)


class TestObjectCopy(GlobalCategoryTestData, TestCase):
    def test_object_copy(self):
        category_count = Category.objects.count()
        self.assertEqual(category_count, 3)

        category = Category.objects.last()
        category.pk = None
        category.save()

        category_count = Category.objects.count()
        self.assertEqual(category_count, 4)
        self.assertEqual(Category.objects.last().name, "Mortal")


class TestSingleObjectCreate(TestCase):
    def test_single_object_create(self):
        Origin.objects.create(name="origin 1")
        self.assertEqual(Origin.objects.count(), 1)

        try:
            Origin.objects.create(name="origin 2")
        except IntegrityError:
            pass
        self.assertEqual(Origin.objects.count(), 1)
