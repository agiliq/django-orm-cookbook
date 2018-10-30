How to use a UUID instead of ID as primary key?
++++++++++++++++++++++++++++++++++++++++++++++++++

Whenever we create any new model, there is an ID field attached to it. The ID field's data type will be Integer by default.

To make id field as UUID, there is a new field type UUIDField which was added in django version 1.8+.

Example ::

    import uuid
    from django.db import models

    class Event(models.Model):
        id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
        details = models.TextField()
        years_ago = models.PositiveIntegerField()

    >>> eventobject = Event.objects.all()
    >>> eventobject.first().id
    '3cd2b4b0c36f43488a93b3bb72029f46'
