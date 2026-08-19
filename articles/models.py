from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse
from baseapp.models import BaseModel

User = get_user_model()

class Category(BaseModel):
    title = models.CharField(max_length=255)
    description = models.CharField(max_length=255, blank=True, null=True)
    slug = models.SlugField(unique=True)

    class Meta:
        db_table = 'categories'

    def __str__(self):
        return self.title


class Tag(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)

    class Meta:
        db_table = 'tags'

    def __str__(self):
        return self.name


class Article(BaseModel):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='articles')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='articles')
    title = models.CharField(max_length=255)
    image = models.CharField(max_length=255, blank=True, null=True)
    description = models.CharField(max_length=500, blank=True, null=True)
    article = models.TextField()
    slug = models.SlugField(unique=True)
    views_count = models.BigIntegerField(default=0)
    tags = models.ManyToManyField(Tag, through='ArticleTag', related_name='articles')

    class Meta:
        db_table = 'articles'

    def get_absolute_url(self):
        return reverse('article-detail', kwargs={'pk': self.pk})

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