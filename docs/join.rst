두 모델을 결합(JOIN)하려면 어떻게 하나요?
========================================================

SQL에서는 JOIN 문을 이용해 동일한 값을 가진 열을 기준으로 두 표를 결합할 수 있습니다. 결합 연산은 여러 가지 방법으로 수행할 수 있습니다. 다음은 장고에서 이를 수행하는 몇 가지 예입니다. ::

    >>> a1 = Article.objects.select_related('reporter') // Using select_related
    >>> a1
    <QuerySet [<Article: International News>, <Article: Local News>, <Article: Morning news>, <Article: Prime time>, <Article: Test Article>, <Article: Weather Report>]>
    >>> print(a1.query)
    SELECT "events_article"."id", "events_article"."headline", "events_article"."pub_date", "events_article"."reporter_id", "events_article"."slug", "auth_user"."id", "auth_user"."password", "auth_user"."last_login", "auth_user"."is_superuser", "auth_user"."username", "auth_user"."first_name", "auth_user"."last_name", "auth_user"."email", "auth_user"."is_staff", "auth_user"."is_active", "auth_user"."date_joined" FROM "events_article" INNER JOIN "auth_user" ON ("events_article"."reporter_id" = "auth_user"."id") ORDER BY "events_article"."headline" ASC
    >>> a2 = Article.objects.filter(reporter__username='John')
    >>> a2
    <QuerySet [<Article: International News>, <Article: Local News>, <Article: Prime time>, <Article: Test Article>, <Article: Weather Report>]>
    >>> print(a2.query)
    SELECT "events_article"."id", "events_article"."headline", "events_article"."pub_date", "events_article"."reporter_id", "events_article"."slug" FROM "events_article" INNER JOIN "auth_user" ON ("events_article"."reporter_id" = "auth_user"."id") WHERE "auth_user"."username" = John ORDER BY "events_article"."headline" ASC
