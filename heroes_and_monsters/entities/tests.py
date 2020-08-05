from django.db.models import OuterRef, Subquery
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
