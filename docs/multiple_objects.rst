How to create multiple objects in one shot?
++++++++++++++++++++++++++++++++++++++++++++++++++

There are conditions when we want to save multiple objects in one go. Say we want to add multiple categories at once and we don't want to make many queries to the database.
We can use django-ORM's builtin method bulk_create for creating multiple objects at one shot.

Code ::

    >>> Category.objects.all().count()
    2
    >>> Category.objects.bulk_create([Category(name="Foods Items"), Category(name="Fruits"), Category(name="Vegetables")])
    [<Category: Foods Items>, <Category: Fruits>, <Category: Vegetables>]
    >>> Category.objects.all().count()
    5
