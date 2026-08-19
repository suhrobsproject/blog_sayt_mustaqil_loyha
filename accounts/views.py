from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.contrib.auth import authenticate, login, update_session_auth_hash, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import CustomUserForm, LoginForm, ProfileForm, CustomPasswordChangeForm
from articles.models import Article, Category
from .models import CustomUser


def home(request):
    categories = Category.objects.all()
    latest_articles = Article.objects.select_related('author', 'category').order_by('-created_at')[:9]
    popular_articles = Article.objects.order_by('-viewscount')[:5]
    context = {
        'categories': categories,
        'latest_articles': latest_articles,
        'popular_articles': popular_articles
    }
    return render(request, 'index.html', context)


class RegisterView(View):
    def get(self, request):
        if request.user.is_authenticated:
            return redirect('accounts:profile')
        form = CustomUserForm()
        return render(request, 'accounts/register.html', {'form': form})

    def post(self, request):
        form = CustomUserForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            form.save()
            return redirect('accounts:login')
        return render(request, 'accounts/register.html', {'form': form})


class LoginView(View):
    def get(self, request):
        if request.user.is_authenticated:
            return redirect('accounts:profile')
        form = LoginForm()
        return render(request, 'accounts/login.html', {'form': form})

    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                return redirect('accounts:profile')
            else:
                form.add_error(None, "Foydalanuvchi nomi yoki parol notoʻgʻri!")

        return render(request, 'accounts/login.html', {'form': form})


class CustomLogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('accounts:home')


class ProfileView(LoginRequiredMixin, View):
    login_url = 'accounts:login'

    def get(self, request):
        user_articles = Article.objects.filter(author=request.user).order_by('-created_at')
        return render(request, 'accounts/profile.html', {'user': request.user, 'user_articles': user_articles})


class ProfileUpdateView(LoginRequiredMixin, View):
    login_url = 'accounts:login'

    def get(self, request):
        form = ProfileForm(instance=request.user)
        return render(request, 'accounts/profile_update.html', {'form': form})

    def post(self, request):
        form = ProfileForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('accounts:profile')
        return render(request, 'accounts/profile_update.html', {'form': form})


class CustomPasswordChangeView(LoginRequiredMixin, View):
    login_url = 'accounts:login'

    def get(self, request):
        form = CustomPasswordChangeForm(user=request.user)
        return render(request, 'accounts/password_change.html', {'form': form})

    def post(self, request):
        form = CustomPasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            new_password = form.cleaned_data.get('new_password')
            request.user.set_password(new_password)
            request.user.save()
            update_session_auth_hash(request, request.user)
            return redirect('accounts:profile')
        return render(request, 'accounts/password_change.html', {'form': form})



class UserProfileDetailView(View):
    def get(self, request, username):
        author = get_object_or_404(CustomUser, username=username)
        author_articles = Article.objects.filter(author=author).order_by('-created_at')
        return render(request, 'accounts/user_profile.html', {
            'author': author,
            'author_articles': author_articles
        })