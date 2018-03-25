How to model many to many relationships?
===============================================

A many-to-many relationship refers to a relationship between tables in a database when a parent row in one table contains several child rows in the second table, and vice versa.

Just to make it more interactive, we will talk about a twitter app. By just using few fields and ManyToMany field we can make a simple twitter app.

We basically have 3 basic things in Twitter, tweets, followers, favourite/unfavourite.

We have two models to make everything work. We are inheriting django's auth_user.::

    class User(AbstractUser):
        tweet = models.ManyToManyField(Tweet, blank=True)
        follower = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True)
        pass

    class Tweet(models.Model):
        tweet = models.TextField()
        favourite = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True, related_name='user_favourite')

        def __unicode__(self):
            return self.tweet

What will the above model be able to do ? ::

    1) User will able to follow/unfollow other users.
    2) User will able to see tweets made by other users whom user is following.
    3) User is able to favorite/unfavorite tweets.


Few operations using ManyToManyfield which can be done are: ::

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

We have created few tweets and few users, that didn't involve any use of M2M field so far. Lets continue linking them in next step. ::

    >>> u2.tweet.add(t1)
    >>> u2.save()
    >>> u2.tweet.add(t2)
    >>> u2.save()
    // User can follow other users.
    >>> u2.follow.add(u1)
    >>> u2.save()
    // Tweets are linked to the users. Users have folloewd each other. Now we can make users do favourite/unfavourite of the tweets.
    >>> t1.favourite.add(u1)
    >>> t1.save()
    >>> t1.favourite.add(u3)
    >>> t1.save()
    // For removing any users vote
    >>> t1.favourite.remove(u1)
    >>> t1.save()

Working example can be found in the repo: https://github.com/yashrastogi16/simpletwitter
