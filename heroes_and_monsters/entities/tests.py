from django.contrib.auth.models import User
from django.db.models import OuterRef, Subquery, F
from django.db.models.functions import Substr
from django.test import TestCase

from events.tests import GlobalUserTestData
from .models import Hero, Category, Origin


class TestSubQuery(TestCase):
    def setUp(self):
        Category.objects.bulk_create(
            [
                Category(name="category_1", hero_count=12, villain_count=15),
                Category(name="category_2", hero_count=25, villain_count=5),
                Category(name="category_3", hero_count=17, villain_count=13),
            ]
        )
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
        output_category = ["category_1", "category_2", "category_3"]
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


class TestBulkCreate(TestCase):
    def test_bulk_create(self):
        category_count = Category.objects.all().count()
        self.assertEqual(category_count, 0)
        Category.objects.bulk_create(
            [
                Category(name="God", hero_count=0, villain_count=0),
                Category(name="Demi God", hero_count=0, villain_count=0),
                Category(name="Mortal", hero_count=0, villain_count=0),
            ]
        )
        category_count = Category.objects.all().count()
        self.assertEqual(category_count, 3)
