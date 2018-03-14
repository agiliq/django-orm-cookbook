from django.test import TestCase
from .models import User

# Create your tests here.
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

