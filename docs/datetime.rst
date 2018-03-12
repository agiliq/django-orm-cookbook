How to convert string to datetime and store in database?
============================================================

We can convert a date-string and store it in the database using django in many ways. Few of them are discussed below.
Lets say we have a date-string as "2018-03-11" we can not directly store it to our date field, so we can use some dateparser or python library for it. ::

    >>> user = User.objects.get(id=1)
    >>> date_str = "2018-03-11"
    >>> from django.utils.dateparse import parse_date // Way 1
    >>> temp_date = parse_date(date_str)
    >>> a1 = Article(headline="String converted to date", pub_date=temp_date, reporter=user)
    >>> a1.save()
    >>> a1.pub_date
    datetime.date(2018, 3, 11)
    >>> from datetime import datetime // Way 2
    >>> temp_date = datetime.strptime(date_str, "%Y-%m-%d").date()
    >>> a2 = Article(headline="String converted to date way 2", pub_date=temp_date, reporter=user)
    >>> a2.save()
    >>> a2.pub_date
    datetime.date(2018, 3, 11)


