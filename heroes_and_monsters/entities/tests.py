from django.contrib.auth.models import User
from django.db.models import OuterRef, Subquery, F, Count
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


class GlobalHeroTestData(GlobalCategoryTestData):
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


class TestSubQuery(GlobalHeroTestData, TestCase):
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


class TestDenormalizedColumnUpdate(GlobalHeroTestData, TestCase):
    def test_hero_count(self):
        category = Category.objects.get(id=2)

        hero_count = category.hero_count
        Hero.objects.create(
            name="Iron Man",
            description="Iron Man",
            benevolence_factor=90,
            category_id=2,
            origin_id=1,
        )
        category = Category.objects.get(id=2)

        self.assertEqual(category.hero_count, hero_count + 1)


class TestTruncateQuery(GlobalCategoryTestData, TestCase):
    def test_truncate_data(self):
        self.assertEqual(Category.objects.all().count(), 3)
        Category.objects.all().delete()
        self.assertEqual(Category.objects.all().count(), 0)

    def test_truncate_data_using_cursor(self):
        self.assertEqual(Category.objects.all().count(), 3)
        Category.truncate()
        self.assertEqual(Category.objects.all().count(), 0)


class TestOrderBy(GlobalHeroTestData, TestCase):
    def test_orderby_on_related_field(self):
        hereos = Hero.objects.all().order_by(
            'category__name', 'name'
        ).values_list("name", flat=True)
        output_hereos = ['Poseidon', 'Xeus', 'ZeuX', 'Zeus']

        self.assertEqual(list(hereos), output_hereos)

    def test_orderby_on_annotate(self):
        categories = Category.objects.annotate(
            hero_count_annotate=Count("hero")
        ).order_by(
            "-hero_count_annotate"
        ).values_list("name", flat=True)
        output_category = ['Demi God', 'God', 'Mortal']

        self.assertEqual(list(categories), output_category)