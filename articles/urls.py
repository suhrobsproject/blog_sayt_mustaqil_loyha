from django.urls import path
from .views import (
    ArticleListView,
    ArticleDetailView,
    ArticleCreateView,
    ArticleUpdateView,
    ArticleDeleteView
)

urlpatterns = [
    path('article-list', ArticleListView.as_view(), name='article-list'),
    path('article_create/', ArticleCreateView.as_view(), name='article-create'),
    path('article_detail/<int:pk>/', ArticleDetailView.as_view(), name='article-detail'),
    path('<int:pk>/update/', ArticleUpdateView.as_view(), name='article-update'),
    path('<int:pk>/delete/', ArticleDeleteView.as_view(), name='article-delete'),
]