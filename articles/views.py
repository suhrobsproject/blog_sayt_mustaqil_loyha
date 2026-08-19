from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect, get_object_or_404
from .models import Article
from .forms import ArticleForm

class ArticleListView(View):
    """Barcha maqolalar ro'yxati"""
    def get(self, request):
        articles = Article.objects.all().order_by('-created_at')
        return render(request, 'articles/article_list.html', {'articles': articles})


class ArticleDetailView(View):
    """Bitta maqolani batafsil ko'rsatish va ko'rishlar sonini oshirish"""
    def get(self, request, pk):
        article = get_object_or_404(Article, pk=pk)
        article.views_count += 1
        article.save(update_fields=['views_count'])
        return render(request, 'articles/article_detail.html', {'article': article})


class ArticleCreateView(LoginRequiredMixin, View):
    """Yangi maqola yozish (Faqat tizimga kirganlar uchun)"""
    def get(self, request):
        form = ArticleForm()
        return render(request, 'articles/article_form.html', {'form': form})

    def post(self, request):
        form = ArticleForm(request.POST)
        if form.is_valid():
            article = form.save(commit=False)
            article.author = request.user
            article.save()
            return redirect(article.get_absolute_url())
        return render(request, 'articles/article_form.html', {'form': form})


class ArticleUpdateView(LoginRequiredMixin, View):
    """Maqolani tahrirlash"""
    def get(self, request, pk):
        article = get_object_or_404(Article, pk=pk, author=request.user)
        form = ArticleForm(instance=article)
        return render(request, 'articles/article_form.html', {'form': form, 'article': article})

    def post(self, request, pk):
        article = get_object_or_404(Article, pk=pk, author=request.user)
        form = ArticleForm(request.POST, instance=article)
        if form.is_valid():
            form.save()
            return redirect(article.get_absolute_url())
        return render(request, 'articles/article_form.html', {'form': form, 'article': article})


class ArticleDeleteView(LoginRequiredMixin, View):
    """Maqolani o'chirish"""
    def post(self, request, pk):
        article = get_object_or_404(Article, pk=pk, author=request.user)
        article.delete()
        return redirect('article-list')