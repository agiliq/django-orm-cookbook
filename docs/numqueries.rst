질의 횟수가 고정된 횟수만큼만 일어나는지 확인할 수 있을까요?
=======================================================================================

장고 단위 테스트 클래스의 `assertNumQueries()` 메서드를 사용하여 데이터베이스에 발생하는 질의 횟수를 검증할 수 있습니다.

.. code-block:: python

  def test_number_of_queries(self):
      User.objects.create(username='testuser1', first_name='Test', last_name='user1')
      # 위 ORM 명령으로 질의 횟수가 1 번 일어나야 한다.
      self.assertNumQueries(1)
      User.objects.filter(username='testuser').update(username='test1user')
      # 질의 횟수가 한 번 증가해야 한다.
      self.assertNumQueries(2)
