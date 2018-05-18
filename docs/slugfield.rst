How to use slug field with django for more readability?
+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

Slug is a part of a URL which identifies a particular page on a website in a form readable by users. For making it work django offers us a slugfield. It can be implimented as under.
We already had a model :code:`Article` we will be adding slugfield to it to make it user readable. ::

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
    // slug here is auto-generated, we haven't created it in the above create method.
    >>> a1.slug
    'todays-market-report'

Slug is useful because:
    | it's human friendly (eg. /blog/ instead of /1/).
    | it's good SEO to create consistency in title, heading and URL.
