from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.utils.text import slugify
from baseapp.models import BaseModel

User = get_user_model()

class Category(BaseModel):
    title = models.CharField(max_length=255)
    description = models.CharField(max_length=255, blank=True, null=True)
    slug = models.SlugField(unique=True, blank=True)

    class Meta:
        db_table = 'categories'
        verbose_name_plural = 'Categories'

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class Tag(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, blank=True)

    class Meta:
        db_table = 'tags'

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Article(BaseModel):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='articles')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='articles')
    title = models.CharField(max_length=255)
    # Fayl sifatida yuklanadigan rasm maydoni
    image = models.ImageField(upload_to='articles/', blank=True, null=True)
    description = models.CharField(max_length=500, blank=True, null=True)
    article = models.TextField()
    slug = models.SlugField(unique=True, blank=True)
    viewscount = models.BigIntegerField(default=0)
    tags = models.ManyToManyField(Tag, through='ArticleTag', related_name='articles', blank=True)

    class Meta:
        db_table = 'articles'

    # ... qolgan metodlar o'zgarishsiz qoladi
    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.title)
            slug = base_slug
            counter = 1
            while Article.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('articles:article-detail', kwargs={'pk': self.pk})

    def __str__(self):
        return self.title


class ArticleTag(models.Model):
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)
    article = models.ForeignKey(Article, on_delete=models.CASCADE)

    class Meta:
        db_table = 'article_tags'


class Comment(BaseModel):
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    comment = models.TextField()
    parent = models.ForeignKey('self', on_delete=models.CASCADE, blank=True, null=True, related_name='replies')

    class Meta:
        db_table = 'comments'

    def __str__(self):
        return f"{self.user} - {self.comment[:20]}"