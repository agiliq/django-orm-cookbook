How to assert that a function used a fixed number of queries?
========================================================================

We can count number of queries for testing by using :code:`assertNumQueries()` method. ::

        def test_number_of_queries(self):
            User.objects.create(username='testuser1', first_name='Test', last_name='user1')
            # Above ORM create will run only one query.
            self.assertNumQueries(1)
            User.objects.filter(username='testuser').update(username='test1user')
            # One more query added.
            self.assertNumQueries(2)
