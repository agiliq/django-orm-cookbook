슬러그 필드를 사용할 수 있나요?
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

슬러그(`slug`)는 URL의 구성요소로 웹사이트의 특정 페이지를 가리키는 사람이 읽기 쉬운 형식의 식별자입니다. 장고에서는 슬러그 필드(:code:`SlugField`)로 슬러그를 지원합니다. 다음 예에서 사용법을 확인하실 수 있습니다. 앞서 살펴보았던 :code:`Article` 모델에 슬러그 필드를 추가해 가독성을 높여 보았습니다. ::


    from django.utils.text import slugify
    class Article(models.Model):
        headline = models.CharField(max_length=100)
        . . .
        slug = models.SlugField(unique=True)

        def save(self, *args, **kwargs):
            self.slug = slugify(self.headline)
            super(Article, self).save(*args, **kwargs)
        . . .

    >>> u1 = User.objects.get(id=1)
    >>> from datetime import date
    >>> a1 = Article.objects.create(headline="todays market report", pub_date=date(2018, 3, 6), reporter=u1)
    >>> a1.save()
    # 슬러그는 자동으로 생성됩니다. create 메서드를 따로 정의한 게 아닙니다.
    >>> a1.slug
    'todays-market-report'

슬러그의 장점:
    | 사람이 이해하기 좋다. (:code:`/1/` 보다 :code:`/blog/` 가 좋다)
    | 제목과 URL을 동일하게 맞춰 검색엔진 최적화(SEO)에 도움이 된다.
