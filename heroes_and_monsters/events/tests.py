import unittest

from django.db.models import Q, Subquery
from django.db.utils import OperationalError
from django.test import TestCase
from .models import User, Event, EventVillain, UserParent


class GlobalUserTestData:

    def setUp(self):
        User.objects.bulk_create([User(username="yash", first_name="Yash", last_name="Rastogi", email="yash@agiliq.com"), User(username="John", first_name="John", last_name="Kumar", email="john@gmail.com"), User(username="Ricky", first_name="Ricky", last_name="Dayal", email="ricky@gmail.com"), User(username="sharukh", first_name="Sharukh", last_name="Misra", email="sharukh@hotmail.com"), User(username="Ritesh", first_name="Ritesh", last_name="Deshmukh", email="ritesh@yahoo.com"), User(username="Billy", first_name="Billy", last_name="sharma", email="billy@gmail.com"), User(username="Radha", first_name="Radha", last_name="George", email="radha@gmail.com"), User(username="sohan", first_name="Sohan", last_name="Upadhyay", email="sohan@aol.com"), User(username="Raghu", first_name="Raghu", last_name="Khan", email="raghu@rediffmail.com"), User(username="rishab", first_name="Rishabh", last_name="Deol", email="rishabh@yahoo.com")])


class TestORM(TestCase):

    def test_update_result(self):
        userobject = User.objects.create(username='testuser', first_name='Test', last_name='user')
        User.objects.filter(username='testuser').update(username='test1user')
        # At this point userobject.val is still testuser, but the value in the database
        # was updated to test1user. The object's updated value needs to be reloaded
        # from the database.
        userobject.refresh_from_db()
        self.assertEqual(userobject.username, 'test1user')

    def test_number_of_queries(self):
        User.objects.create(username='testuser1', first_name='Test', last_name='user1')
        # Above ORM create will run only one query.
        self.assertNumQueries(1)
        User.objects.filter(username='testuser').update(username='test1user')
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
            first_name__startswith='R',
            last_name__startswith='D'
        )
        self.queryset_2 = User.objects.filter(
            first_name__startswith='R'
        ) & User.objects.filter(
            last_name__startswith='D'
        )
        self.queryset_3 = User.objects.filter(
            Q(first_name__startswith='R') &
            Q(last_name__startswith='D')
        )

    def test_query(self):
        output_names = ['Ricky', 'Ritesh', 'Rishabh']

        self.assertEqual(self.queryset_1.count(), 3)
        self.assertEqual(list(self.queryset_1.values_list("first_name", flat=True)), output_names)

        self.assertEqual(self.queryset_2.count(), 3)
        self.assertEqual(list(self.queryset_2.values_list("first_name", flat=True)), output_names)

        self.assertEqual(self.queryset_3.count(), 3)
        self.assertEqual(list(self.queryset_3.values_list("first_name", flat=True)), output_names)

    def test_different_query_are_same(self):
        self.assertTrue(str(self.queryset_1.query) == str(self.queryset_2.query) == str(self.queryset_3.query))


class TestORQuery(GlobalUserTestData, TestCase):

    def setUp(self):
        super().setUp()
        self.queryset_1 = User.objects.filter(
                first_name__startswith='R'
            ) | User.objects.filter(
            last_name__startswith='D'
        )
        self.queryset_2 = User.objects.filter(Q(first_name__startswith='R')|Q(last_name__startswith='D'))

    def test_or_query(self):
        output_names = ['Ricky', 'Ritesh', 'Radha', 'Raghu', 'Rishabh']

        self.assertEqual(self.queryset_1.count(), 5)
        self.assertEqual(list(self.queryset_1.values_list("first_name", flat=True)), output_names)

        self.assertEqual(self.queryset_2.count(), 5)
        self.assertEqual(list(self.queryset_2.values_list("first_name", flat=True)), output_names)

    def test_different_query_are_same(self):
        self.assertTrue(str(self.queryset_1.query) == str(self.queryset_2.query))


class TestNotQuery(GlobalUserTestData, TestCase):

    def test_not_query(self):
        self.queryset = User.objects.filter(~Q(id__lt=5))

        output_names = ['Ritesh', 'Billy', 'Radha', 'Sohan', 'Raghu', 'Rishabh']

        self.assertEqual(self.queryset.count(), 6)
        self.assertEqual(list(self.queryset.values_list("first_name", flat=True)), output_names)


class TestUnionQuery(GlobalUserTestData, TestCase):

    def setUp(self):
        super().setUp()
        self.q1 = User.objects.filter(id__gte=5)
        self.q2 = User.objects.filter(id__lte=9)
        self.q3 = self.q1.union(self.q2)
        self.q4 = self.q2.union(self.q1)

    def test_union_query(self):        
        output_names = ['Billy', 'John', 'Radha', 'Raghu', 'Ricky', 'Rishabh', 'Ritesh', 'Sharukh', 'Sohan', 'Yash']

        self.assertEqual(self.q3.count(), 10)
        self.assertEqual(self.q4.count(), 10)
        self.assertEqual(list(self.q3.values_list("first_name", flat=True)), output_names)
        self.assertEqual(list(self.q4.values_list("first_name", flat=True)), output_names)

    @unittest.expectedFailure
    def test_union_exception(self):
        q3 = EventVillain.objects.all()
        self.assertRaises(OperationalError, self.q1.union(q3))


class TestSomeFieldQuery(GlobalUserTestData, TestCase):

    def test_values(self):
        queryset = User.objects.filter(
            first_name__startswith='R'
        ).values('first_name', 'last_name')
        output = [{'first_name': 'Ricky', 'last_name': 'Dayal'}, {'first_name': 'Ritesh', 'last_name': 'Deshmukh'}, {'first_name': 'Radha', 'last_name': 'George'}, {'first_name': 'Raghu', 'last_name': 'Khan'}, {'first_name': 'Rishabh', 'last_name': 'Deol'}]
        self.assertEqual(queryset.count(), 5)
        self.assertEqual(list(queryset), output)

    def test_only(self):
        queryset = User.objects.filter(
            first_name__startswith='R'
        ).only("first_name", "last_name")
        self.assertEqual(queryset.count(), 5)


class TestSubQuery(GlobalUserTestData, TestCase):

    def setUp(self):
        super().setUp()
        u1 = User.objects.get(first_name='Ritesh', last_name='Deshmukh')
        u2 = User.objects.get(first_name='Sohan', last_name='Upadhyay')
        p1 = UserParent(user=u1, father_name='Vilasrao Deshmukh', mother_name='Vaishali Deshmukh')
        p1.save()
        p2 = UserParent(user=u2, father_name='Mr R S Upadhyay', mother_name='Mrs S K Upadhyay')
        p2.save()

    def test_sub_query(self):
        users = User.objects.all()
        queryset = UserParent.objects.filter(user_id__in=Subquery(users.values('id')))

        self.assertEqual(list(queryset.values_list("user_id", flat=True)), [5, 8])
