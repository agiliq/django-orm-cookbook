How to model one to one relationships?
===============================================

One-to-one relationships occur when there is exactly one record in the first table that corresponds to one record in the related table.
Here we have an example where we know that each individual can have only one Biological parents i.e., Mother and Father.
We already have auth user model with us, we will add a new model UserParent as described below. ::

    from django.contrib.auth.models import User

    class UserParent(models.Model):
        user = models.OneToOneField(
            User,
            on_delete=models.CASCADE,
            primary_key=True,
        )
        father_name = models.CharField(max_length=100)
        mother_name = models.CharField(max_length=100)

    >>> u1 = User.objects.get(first_name='Ritesh', last_name='Deshmukh')
    >>> u2 = User.objects.get(first_name='Sohan', last_name='Upadhyay')
    >>> p1 = UserParent(user=u1, father_name='Vilasrao Deshmukh', mother_name='Vaishali Deshmukh')
    >>> p1.save()
    >>> p1.user.first_name
    'Ritesh'
    >>> p2 = UserParent(user=u2, father_name='Mr R S Upadhyay', mother_name='Mrs S K Upadhyay')
    >>> p2.save()
    >>> p2.user.last_name
    'Upadhyay'

The on_delete method is used to tell Django what to do with model instances that depend on the model instance you delete. (e.g. a ForeignKey relationship). The on_delete=models.CASCADE tells Django to cascade the deleting effect i.e. continue deleting the dependent models as well. ::

    >>> u2.delete()

Will also delete the related record of UserParent.
