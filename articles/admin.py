from django.contrib import admin
from .models import Category, Tag, Article, Comment, ArticleTag

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'created_at')
    prepopulated_fields = {'slug': ('title',)}

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}

class ArticleTagInline(admin.TabularInline):
    model = ArticleTag
    extra = 1

@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'author', 'viewscount', 'created_at')
    list_filter = ('category', 'created_at')
    search_fields = ('title', 'description', 'article')
    inlines = [ArticleTagInline]

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('user', 'article', 'parent', 'created_at')
    search_fields = ('comment', 'user__username')