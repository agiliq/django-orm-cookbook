함수가 고정된 개수의 쿼리를 실행하는지 확인하는 방법은?
========================================================================

테스트에서 ``assertNumQueries()`` 메서드를 사용하면 쿼리의 개수를 확인할 수 있습니다.

.. code-block:: python

  def test_number_of_queries(self):
      User.objects.create(username='testuser1', first_name='Test', last_name='user1')
      # 위의 ORM은 하나의 쿼리를 실행할 것입니다.
      self.assertNumQueries(1)
      User.objects.filter(username='testuser').update(username='test1user')
      # 쿼리가 하나 더 추가되었습니다.
      self.assertNumQueries(2)
