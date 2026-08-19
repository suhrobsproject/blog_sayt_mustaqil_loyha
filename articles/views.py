from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import F, Q
from .models import Article, Category, Comment, Tag
from .forms import ArticleForm, CommentForm


class ArticleListView(View):
    def get(self, request):
        query = request.GET.get('q', '').strip()
        category_slug = request.GET.get('category')
        tag_slug = request.GET.get('tag')

        categories = Category.objects.all()
        tags = Tag.objects.all()
        articles = Article.objects.select_related('author', 'category').prefetch_related('tags').order_by('-created_at')

        if query:
            articles = articles.filter(
                Q(title__icontains=query) |
                Q(description__icontains=query) |
                Q(article__icontains=query)
            )

        if category_slug:
            articles = articles.filter(category__slug=category_slug)
        elif tag_slug:
            articles = articles.filter(tags__slug=tag_slug)

        return render(request, 'articles/article_list.html', {
            'articles': articles,
            'categories': categories,
            'tags': tags,
            'current_category': category_slug,
            'current_tag': tag_slug,
            'query': query
        })


class ArticleDetailView(View):
    def get(self, request, pk):
        article = get_object_or_404(Article.objects.select_related('author', 'category').prefetch_related('tags'), pk=pk)
        Article.objects.filter(pk=pk).update(viewscount=F('viewscount') + 1)
        article.refresh_from_db(fields=['viewscount'])

        comments = article.comments.filter(parent__isnull=True).select_related('user').prefetch_related('replies__user').order_by('-created_at')
        form = CommentForm()
        return render(request, 'articles/article_detail.html', {
            'article': article,
            'comments': comments,
            'form': form
        })

    def post(self, request, pk):
        if not request.user.is_authenticated:
            return redirect('accounts:login')

        article = get_object_or_404(Article, pk=pk)
        form = CommentForm(request.POST)
        if form.is_valid():
            parent_id = form.cleaned_data.get('parent_id')
            parent_obj = Comment.objects.filter(id=parent_id).first() if parent_id else None

            comment = form.save(commit=False)
            comment.article = article
            comment.user = request.user
            comment.parent = parent_obj
            comment.save()
            return redirect('articles:article-detail', pk=pk)

        comments = article.comments.filter(parent__isnull=True).select_related('user').prefetch_related('replies__user').order_by('-created_at')
        return render(request, 'articles/article_detail.html', {
            'article': article,
            'comments': comments,
            'form': form
        })


class ArticleCreateView(LoginRequiredMixin, View):
    login_url = 'accounts:login'

    def get(self, request):
        form = ArticleForm()
        return render(request, 'articles/article_form.html', {'form': form, 'title': "Yangi IT maqola yozish"})

    def post(self, request):
        form = ArticleForm(request.POST, request.FILES)
        if form.is_valid():
            article = form.save(commit=False)
            article.author = request.user
            article.save()
            form.save_m2m()
            return redirect(article.get_absolute_url())
        return render(request, 'articles/article_form.html', {'form': form, 'title': "Yangi IT maqola yozish"})


class ArticleUpdateView(LoginRequiredMixin, UserPassesTestMixin, View):
    login_url = 'accounts:login'

    def test_func(self):
        article = get_object_or_404(Article, pk=self.kwargs['pk'])
        return self.request.user == article.author or self.request.user.is_staff

    def get(self, request, pk):
        article = get_object_or_404(Article, pk=pk)
        form = ArticleForm(instance=article)
        return render(request, 'articles/article_form.html', {'form': form, 'article': article, 'title': "Maqolani tahrirlash"})

    def post(self, request, pk):
        article = get_object_or_404(Article, pk=pk)
        form = ArticleForm(request.POST, request.FILES, instance=article)
        if form.is_valid():
            updated_article = form.save(commit=False)
            if not request.FILES.get('image'):
                updated_article.image = article.image
            updated_article.save()
            form.save_m2m()
            return redirect(updated_article.get_absolute_url())
        return render(request, 'articles/article_form.html', {'form': form, 'article': article, 'title': "Maqolani tahrirlash"})


class ArticleDeleteView(LoginRequiredMixin, UserPassesTestMixin, View):
    login_url = 'accounts:login'

    def test_func(self):
        article = get_object_or_404(Article, pk=self.kwargs['pk'])
        return self.request.user == article.author or self.request.user.is_staff

    def post(self, request, pk):
        article = get_object_or_404(Article, pk=pk)
        article.delete()
        return redirect('articles:article-list')