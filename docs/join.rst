Django ORM에서 join 연산이 어떻게 작동하나요?
======================================================

SQL Join문은 둘 이상의 테이블 사이에서 공통 필드를 기반으로 데이터 혹은 행을 결합하는 데 사용됩니다. Join은 여러 방법으로 수행될 수 있으며 몇가지 예시는 아래와 같습니다. ::

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
