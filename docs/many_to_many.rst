다대다 관계는 어떻게 모델링하는가?
===============================================

| 다대다 관계는 하나의 레코드가 관계테이블의 여러 하위 레코드를 가질 수 있으며, 반대로도 가능합니다.
|
| 인터렉티브한 것을 만들기 위해서, 트위터 앱에 관해 이야기 하려고 합니다.
| 우리는 몇 개의 필드와 ManyToMany 필드를 이용하여 간단한 트위터 앱을 만들 수 있습니다.
| 트위터에는 트윗, 팔로워, 마음에 들어요/마음에 들어요 취소 와 같은 세 가지 기본적인 항목이 있습니다.
|
| 여기에 이 모든 것이 작동하는 두 개의 모델이 있습니다. 우리는 여기서 Django의 auth_user를 상속할 것입니다.

.. code-block :: python

    class User(AbstractUser):
        tweet = models.ManyToManyField(Tweet, blank=True)
        follower = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True)
        pass

    class Tweet(models.Model):
        tweet = models.TextField()
        favorite = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True, related_name='user_favorite')

        def __unicode__(self):
            return self.tweet

위에 정의된 모델은 어떤 것이 가능할까요?

::

    1) 사용자는 다른 사용자를 팔로우/팔로우 취소를 할 수 있습니다.
    2) 사용자는 팔로잉하고 있는 사용자가 작성한 트윗을 볼 수 있습니다.
    3) 사용자는 트윗에 마음에 들어요/마음에 들어요 취소를 할 수 있습니다.

다대다 관계를 사용하여 수행할 수 있는 몇 가지 작업이 있습니다.

>>> t1 = Tweet(tweet="I am happy today")
>>> t1.save()
>>> t2 = Tweet(tweet="This is my second Tweet")
>>> t2.save()
>>> u1 = User(username='johny1', first_name='Johny', last_name='Smith', email='johny@example.com')
>>> u1.save()
>>> u2 = User(username='johny1', first_name='Johny', last_name='Smith', email='johny@example.com')
>>> u2.save()
>>> u3 = User(username='someuser', first_name='Some', last_name='User', email='some@example.com')
>>> u3.save()

| 여기까지는 ManyToMany 필드의 어떤 용법도 사용하지 않은 채, 몇 개의 트윗과 사용자를 생성했습니다.
| 다음에는 이것들을 연결해봅시다.

>>> u2.tweet.add(t1)
>>> u2.save()
>>> u2.tweet.add(t2)
>>> u2.save()
>>> # 사용자는 다른 사용자를 팔로우할 수 있습니다.
>>> u2.follow.add(u1)
>>> u2.save()
>>> # 트윗은 사용자에게 연결되어 있습니다. 이제 사용자들이 트윗에 마음에 들어요/마음에 들어요 취소를 하게 할 수 있습니다.
>>> t1.favorite.add(u1)
>>> t1.save()
>>> t1.favorite.add(u3)
>>> t1.save()
>>> # 사용자가 마음에 들어요 한 것을 취소하려면
>>> t1.favorite.remove(u1)
>>> t1.save()

작동하는 예제는 여기에서 볼 수 있습니다. : https://github.com/yashrastogi16/simpletwitter
