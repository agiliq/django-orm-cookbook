다대다 관계는 어떻게 나타내나요?
===================================================

다대다 관계란 한 표의 항목이 다른 표의 항목 여러 개를 가리킬 수 있고, 반대로 다른 표의 항목이 그 표의 항목을 여러 개 가리킬 수도 있는 관계입니다.

실제로 실행 가능한 예로, 트위터 앱을 다뤄 보겠습니다. 필드 몇 개와 :code:`ManyToMany` 필드만 있으면 간단한 트위터 앱을 만들 수 있습니다.

트위터의 핵심 기능으로 '트윗', '팔로우', '마음에 들어요'가 있습니다. 아래의 두 모델로 그 핵심 기능을 모두 구현할 수 있습니다. :code:`User` 모델은 장고의 사용자 인증 모델을 확장하여 정의했습니다. ::

    class User(AbstractUser):
        tweet = models.ManyToManyField(Tweet, blank=True)
        follower = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True)
        pass

    class Tweet(models.Model):
        tweet = models.TextField()
        favorite = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True, related_name='user_favorite')

        def __unicode__(self):
            return self.tweet

이 모델로 할 수 있는 일은 다음과 같습니다. ::

    1) 사용자가 다른 사용자를 '팔로우' 및 취소할 수 있습니다.
    2) 사용자가 팔로우하는 다른 사용자가 작성한 트윗을 볼 수 있습니다.
    3) 사용자가 트윗에 '마음에 들어요' 및 취소할 수 있습니다.

:code:`ManyToMany` 필드로 수행할 수 있는 연산을 몇 가지 살펴볼 텐데, 그 전에 항목을 몇 개 생성해 둡시다.

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

생성한 항목들을 :code:`ManyToMany` 필드로 연결해 봅시다. ::

>>> u2.tweet.add(t1)
>>> u2.save()
>>> u2.tweet.add(t2)
>>> u2.save()
>>> # 사용자가 다른 사용자를 '팔로우' 할 수 있습니다.
>>> u2.follow.add(u1)
>>> u2.save()
>>> # 트윗이 사용자에 연결되어 있습니다. 사용자들이 트윗에 마음에 들어요 및 취소를 할 수 있습니다.
>>> t1.favorite.add(u1)
>>> t1.save()
>>> t1.favorite.add(u3)
>>> t1.save()
>>> # '마음에 들어요' 취소하기
>>> t1.favorite.remove(u1)
>>> t1.save()

완전히 동작하는 예제는 다음 저장소에서 확인해 주세요.

https://github.com/yashrastogi16/simpletwitter
