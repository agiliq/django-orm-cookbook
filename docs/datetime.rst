시간 정보를 다른 양식으로 변환하여 데이터베이스에 저장하려면 어떻게 해야 하나요?
=============================================================================================

장고에서 시간을 나타내는 텍스트를 다른 양식의 텍스트로 변환하여 데이터베이스에 저장하는 방법은 여러 가지가 있습니다. 몇 가지만 소개하겠습니다.

"2018-03-11"이라는 시간 텍스트가 있는데, 이 양식으로는 데이터베이스에 저장할 수 없다고 가정합시다. 아래와 같이 장고의 dateparser 모듈이나 파이썬 표준 라이브러리를 이용하여 날짜 양식을 변환할 수 있습니다. ::

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


