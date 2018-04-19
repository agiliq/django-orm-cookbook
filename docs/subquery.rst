How to do a subquery experession in Django?
=============================================

Subquery expression which is included in Django from version :code:`1.11`. Lets talk about this with an example. We have a UserParent table which has OnetoOne relation with aut user. We will find all the users having their parents detail saved.

    >>> users = User.objects.all()
    >>> UserParent.objects.filter(user_id__in=Subquery(users.values('id')))
    <QuerySet [<UserParent: UserParent object (2)>, <UserParent: UserParent object (5)>, <UserParent: UserParent object (8)>]>
