모델 객체를 데이터베이스에서 다시 읽어들일 수 있나요?
========================================================================

``refresh_from_db()`` 메서드를 사용하여 데이터베이스에서 모델을 다시 읽어들일 수 있습니다. 값을 갱신하는 테스트를 작성할 때 유용한 기능입니다. 다음 예를 살펴보세요. ::

    class TestORM(TestCase):
        def test_update_result(self):
            userobject = User.objects.create(username='testuser', first_name='Test', last_name='user')
            User.objects.filter(username='testuser').update(username='test1user')
            # 이 때, userobject 인스턴스의 username은 'testuser' 입니다.
            # 그러나 데이터베이스에서는 'test1user'로 수정되었습니다.
            # 모델 인스턴스의 속성이 데이터베이스와 맞지 않으므로 다시 읽어들입니다.
            userobject.refresh_from_db()
            self.assertEqual(userobject.username, 'test1user')
