from datetime import date, datetime
import unittest

from django.db.models import Q, Subquery, Avg, Max, Min, Sum, Count
from django.db.models.functions import Lower
from django.db.utils import OperationalError
from django.test import TestCase
from django.utils.dateparse import parse_date

from .models import User, Event, EventVillain, UserParent, Article, UserParent


class GlobalUserTestData:
    def setUp(self):
        User.objects.bulk_create(
            [
                User(
                    username="yash",
                    first_name="Yash",
                    last_name="Rastogi",
                    email="yash@agiliq.com",
                ),
                User(
                    username="John",
                    first_name="John",
                    last_name="Kumar",
                    email="john@gmail.com",
                ),
                User(
                    username="Ricky",
                    first_name="Ricky",
                    last_name="Dayal",
                    email="ricky@gmail.com",
                ),
                User(
                    username="sharukh",
                    first_name="Sharukh",
                    last_name="Misra",
                    email="sharukh@hotmail.com",
                ),
                User(
                    username="Ritesh",
                    first_name="Ritesh",
                    last_name="Deshmukh",
                    email="ritesh@yahoo.com",
                ),
                User(
                    username="Billy",
                    first_name="Billy",
                    last_name="sharma",
                    email="billy@gmail.com",
                ),
                User(
                    username="Radha",
                    first_name="Radha",
                    last_name="George",
                    email="radha@gmail.com",
                ),
                User(
                    username="sohan",
                    first_name="Sohan",
                    last_name="Upadhyay",
                    email="sohan@aol.com",
                ),
                User(
                    username="Raghu",
                    first_name="Raghu",
                    last_name="Khan",
                    email="raghu@rediffmail.com",
                ),
                User(
                    username="rishab",
                    first_name="Rishabh",
                    last_name="Deol",
                    email="rishabh@yahoo.com",
                ),
            ]
        )


class TestORM(TestCase):
    def test_update_result(self):
        userobject = User.objects.create(
            username="testuser", first_name="Test", last_name="user"
        )
        User.objects.filter(username="testuser").update(username="test1user")
        # At this point userobject.val is still testuser, but the value in the database
        # was updated to test1user. The object's updated value needs to be reloaded
        # from the database.
        userobject.refresh_from_db()
        self.assertEqual(userobject.username, "test1user")

    def test_number_of_queries(self):
        User.objects.create(username="testuser1", first_name="Test", last_name="user1")
        # Above ORM create will run only one query.
        self.assertNumQueries(1)
        User.objects.filter(username="testuser").update(username="test1user")
        # One more query added.
        self.assertNumQueries(2)

    def test_associated_query(self):
        output = 'SELECT "events_event"."id", "events_event"."epic_id", "events_event"."details", "events_event"."years_ago" FROM "events_event"'
        queryset = Event.objects.all()
        self.assertEqual(str(queryset.query), output)


class TestANDQuery(GlobalUserTestData, TestCase):
    def setUp(self):
        super().setUp()
        self.queryset_1 = User.objects.filter(
            first_name__startswith="R", last_name__startswith="D"
        )
        self.queryset_2 = User.objects.filter(
            first_name__startswith="R"
        ) & User.objects.filter(last_name__startswith="D")
        self.queryset_3 = User.objects.filter(
            Q(first_name__startswith="R") & Q(last_name__startswith="D")
        )

    def test_query(self):
        output_names = ["Ricky", "Ritesh", "Rishabh"]

        self.assertEqual(self.queryset_1.count(), 3)
        self.assertEqual(
            list(self.queryset_1.values_list("first_name", flat=True)), output_names
        )

        self.assertEqual(self.queryset_2.count(), 3)
        self.assertEqual(
            list(self.queryset_2.values_list("first_name", flat=True)), output_names
        )

        self.assertEqual(self.queryset_3.count(), 3)
        self.assertEqual(
            list(self.queryset_3.values_list("first_name", flat=True)), output_names
        )

    def test_different_query_are_same(self):
        self.assertTrue(
            str(self.queryset_1.query)
            == str(self.queryset_2.query)
            == str(self.queryset_3.query)
        )


class TestORQuery(GlobalUserTestData, TestCase):
    def setUp(self):
        super().setUp()
        self.queryset_1 = User.objects.filter(
            first_name__startswith="R"
        ) | User.objects.filter(last_name__startswith="D")
        self.queryset_2 = User.objects.filter(
            Q(first_name__startswith="R") | Q(last_name__startswith="D")
        )

    def test_or_query(self):
        output_names = ["Ricky", "Ritesh", "Radha", "Raghu", "Rishabh"]

        self.assertEqual(self.queryset_1.count(), 5)
        self.assertEqual(
            list(self.queryset_1.values_list("first_name", flat=True)), output_names
        )

        self.assertEqual(self.queryset_2.count(), 5)
        self.assertEqual(
            list(self.queryset_2.values_list("first_name", flat=True)), output_names
        )

    def test_different_query_are_same(self):
        self.assertTrue(str(self.queryset_1.query) == str(self.queryset_2.query))


class TestNotQuery(GlobalUserTestData, TestCase):
    def test_not_query(self):
        self.queryset = User.objects.filter(~Q(id__lt=5))

        output_names = ["Ritesh", "Billy", "Radha", "Sohan", "Raghu", "Rishabh"]

        self.assertEqual(self.queryset.count(), 6)
        self.assertEqual(
            list(self.queryset.values_list("first_name", flat=True)), output_names
        )


class TestUnionQuery(GlobalUserTestData, TestCase):
    def setUp(self):
        super().setUp()
        self.q1 = User.objects.filter(id__gte=5)
        self.q2 = User.objects.filter(id__lte=9)
        self.q3 = self.q1.union(self.q2)
        self.q4 = self.q2.union(self.q1)

    def test_union_query(self):
        output_names = [
            "Billy",
            "John",
            "Radha",
            "Raghu",
            "Ricky",
            "Rishabh",
            "Ritesh",
            "Sharukh",
            "Sohan",
            "Yash",
        ]

        self.assertEqual(self.q3.count(), 10)
        self.assertEqual(self.q4.count(), 10)
        self.assertEqual(
            list(self.q3.values_list("first_name", flat=True)), output_names
        )
        self.assertEqual(
            list(self.q4.values_list("first_name", flat=True)), output_names
        )

    @unittest.expectedFailure
    def test_union_exception(self):
        q3 = EventVillain.objects.all()
        self.assertRaises(OperationalError, self.q1.union(q3))


class TestSomeFieldQuery(GlobalUserTestData, TestCase):
    def test_values(self):
        queryset = User.objects.filter(first_name__startswith="R").values(
            "first_name", "last_name"
        )
        output = [
            {"first_name": "Ricky", "last_name": "Dayal"},
            {"first_name": "Ritesh", "last_name": "Deshmukh"},
            {"first_name": "Radha", "last_name": "George"},
            {"first_name": "Raghu", "last_name": "Khan"},
            {"first_name": "Rishabh", "last_name": "Deol"},
        ]
        self.assertEqual(queryset.count(), 5)
        self.assertEqual(list(queryset), output)

    def test_only(self):
        queryset = User.objects.filter(first_name__startswith="R").only(
            "first_name", "last_name"
        )
        self.assertEqual(queryset.count(), 5)


class TestSubQuery(GlobalUserTestData, TestCase):
    def setUp(self):
        super().setUp()
        u1 = User.objects.get(first_name="Ritesh", last_name="Deshmukh")
        u2 = User.objects.get(first_name="Sohan", last_name="Upadhyay")
        p1 = UserParent(
            user=u1, father_name="Vilasrao Deshmukh", mother_name="Vaishali Deshmukh"
        )
        p1.save()
        p2 = UserParent(
            user=u2, father_name="Mr R S Upadhyay", mother_name="Mrs S K Upadhyay"
        )
        p2.save()

    def test_sub_query(self):
        users = User.objects.all()
        queryset = UserParent.objects.filter(user_id__in=Subquery(users.values("id")))

        self.assertEqual(list(queryset.values_list("user_id", flat=True)), [5, 8])


class TestJoinOperation(TestCase):
    def test_join_query(self):
        a1 = Article.objects.select_related("reporter")
        output_query = 'SELECT "events_article"."id", "events_article"."headline", "events_article"."pub_date", "events_article"."reporter_id", "events_article"."slug", "auth_user"."id", "auth_user"."password", "auth_user"."last_login", "auth_user"."is_superuser", "auth_user"."username", "auth_user"."first_name", "auth_user"."last_name", "auth_user"."email", "auth_user"."is_staff", "auth_user"."is_active", "auth_user"."date_joined" FROM "events_article" INNER JOIN "auth_user" ON ("events_article"."reporter_id" = "auth_user"."id") ORDER BY "events_article"."headline" ASC'
        self.assertEqual(str(a1.query), output_query)


class TestSecondLargestRecord(GlobalUserTestData, TestCase):
    def test_second_largest_record(self):
        user = User.objects.order_by("-last_login")[1]
        self.assertEqual(user.username, "John")


class TestDuplicateRecord(GlobalUserTestData, TestCase):
    def setUp(self):
        super().setUp()
        User.objects.create_user(
            username="yash2",
            first_name="Yash",
            last_name="Rastogi2",
            email="yash@example.com",
        )

    def test_duplicate(self):
        duplicates = (
            User.objects.values("first_name")
            .annotate(name_count=Count("first_name"))
            .filter(name_count__gt=1)
        )
        self.assertEqual(list(duplicates), [{"first_name": "Yash", "name_count": 2}])

        records = User.objects.filter(
            first_name__in=[item["first_name"] for item in duplicates]
        )
        self.assertEqual([item.id for item in records], [1, 11])


class TestDistinctRecord(GlobalUserTestData, TestCase):
    def test_distinct_user(self):
        distinct = (
            User.objects.values("first_name")
            .annotate(name_count=Count("first_name"))
            .filter(name_count=1)
        )
        output_user = [
            {"first_name": "Billy", "name_count": 1},
            {"first_name": "John", "name_count": 1},
            {"first_name": "Radha", "name_count": 1},
            {"first_name": "Raghu", "name_count": 1},
            {"first_name": "Ricky", "name_count": 1},
            {"first_name": "Rishabh", "name_count": 1},
            {"first_name": "Ritesh", "name_count": 1},
            {"first_name": "Sharukh", "name_count": 1},
            {"first_name": "Sohan", "name_count": 1},
            {"first_name": "Yash", "name_count": 1},
        ]
        self.assertEqual(list(distinct), output_user)


class TestGroupQuery(GlobalUserTestData, TestCase):
    def test_avg(self):
        avg_id = User.objects.all().aggregate(Avg("id"))
        self.assertEqual(avg_id["id__avg"], 5.5)

    def test_max(self):
        max_id = User.objects.all().aggregate(Max("id"))
        self.assertEqual(max_id["id__max"], 10)

    def test_min(self):
        min_id = User.objects.all().aggregate(Min("id"))
        self.assertEqual(min_id["id__min"], 1)

    def test_sum(self):
        sum_id = User.objects.all().aggregate(Sum("id"))
        self.assertEqual(sum_id["id__sum"], 55)


class TestDateTimeParse(GlobalUserTestData, TestCase):
    def test_str_date_input(self):
        user = User.objects.get(id=1)
        date_str = "2020-08-05"
        temp_date = parse_date(date_str)
        a1 = Article(
            headline="String converted to date", pub_date=temp_date, reporter=user
        )
        a1.save()
        self.assertEqual(a1.id, 1)
        self.assertEqual(a1.pub_date, date(year=2020, month=8, day=5))

        temp_date = datetime.strptime(date_str, "%Y-%m-%d").date()
        a2 = Article(
            headline="String converted to date way 2", pub_date=temp_date, reporter=user
        )
        a2.save()
        a2.pub_date
        self.assertEqual(a2.id, 2)
        self.assertEqual(a2.pub_date, date(year=2020, month=8, day=5))


class TestOrderBy(GlobalUserTestData, TestCase):
    def test_plan_orderby_for_case_insensitive(self):
        users = User.objects.all().order_by(Lower('username')).values_list('username', flat=True)
        output_user = ['Billy', 'John', 'Radha', 'Raghu', 'Ricky', 'rishab', 'Ritesh', 'sharukh', 'sohan', 'yash']
        self.assertEqual(list(users), output_user)

    def test_annotate_orderby_for_case_insensitive(self):
        users = User.objects.annotate(
            uname=Lower('username')
        ).order_by('uname').values_list('username', flat=True)
        output_user = ['Billy', 'John', 'Radha', 'Raghu', 'Ricky', 'rishab', 'Ritesh', 'sharukh', 'sohan', 'yash']
        self.assertEqual(list(users), output_user)

    def test_orderby_on_two_fields(self):
        users = User.objects.all().order_by("is_active", "-last_login", "first_name").values_list("first_name", flat=True)
        output_order = ['Billy', 'John', 'Radha', 'Raghu', 'Ricky', 'Rishabh', 'Ritesh', 'Sharukh', 'Sohan', 'Yash']
        self.assertEqual(list(users), output_order)


class TestModelRelationShip(GlobalUserTestData, TestCase):
    def test_one_to_one_relationship(self):
        u1 = User.objects.get(first_name='Ritesh', last_name='Deshmukh')
        u2 = User.objects.get(first_name='Sohan', last_name='Upadhyay')
        p1 = UserParent(user=u1, father_name='Vilasrao Deshmukh', mother_name='Vaishali Deshmukh')
        p1.save()
        self.assertEqual(p1.user.first_name, 'Ritesh')
        p2 = UserParent(user=u2, father_name='Mr R S Upadhyay', mother_name='Mrs S K Upadhyay')
        p2.save()
        self.assertEqual(p2.user.last_name, 'Upadhyay')

    def test_one_to_many_relationship(self):
        u1 = User(username='johny1', first_name='Johny', last_name='Smith', email='johny@example.com')
        u1.save()
        u2 = User(username='alien', first_name='Alien', last_name='Mars', email='alien@example.com')
        u2.save()
        from datetime import date
        a1 = Article(headline="This is a test", pub_date=date(2018, 3, 6), reporter=u1)
        a1.save()
        self.assertEqual(a1.reporter.id, 11)
        self.assertEqual(a1.reporter.username, "johny1")

        Article.objects.create(headline="This is a test", pub_date=date(2018, 3, 7), reporter=u1)
        articles = Article.objects.filter(reporter=u1)
        self.assertEqual(list(articles.values_list("headline", flat=True)), ["This is a test", "This is a test"])
