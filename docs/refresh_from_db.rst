How to reload a model object from the database?
========================================================================

Models can be reloaded from the databse using :code:`refresh_from_db()` method. THis proves helpful during testing. For example. ::

    class TestORM(TestCase):
        def test_update_result(self):
            userobject = User.objects.create(username='testuser', first_name='Test', last_name='user')
            User.objects.filter(username='testuser').update(username='test1user')
            # At this point userobject.val is still testuser, but the value in the database
            # was updated to test1user. The object's updated value needs to be reloaded
            # from the database.
            userobject.refresh_from_db()
            self.assertEqual(userobject.username, 'test1user')
