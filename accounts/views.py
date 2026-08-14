from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from .models import CustomUser
from .forms import CustomUserForm, LoginForm, ProfileForm, CustomPasswordChangeForm
from django.contrib.auth import authenticate, login, update_session_auth_hash, logout



def home(request):
    return render(request, 'index.html')

class RegisterView(View):

    def get(self, request):
        form = CustomUserForm()
        return render(request, 'accounts/register.html', context={'form':form})

    def post(self, request):

        form = CustomUserForm(data=request.POST, files=request.FILES)

        if form.is_valid():
            form.save()
            return redirect('login')

        return render(request, 'accounts/register.html', context={'form': form})


class LoginView(View):
    def get(self, request):
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
                form.add_error(None, "Username yoki parol noto'g'ri!")

        return render(request, 'accounts/login.html', {'form': form})

class CustomLogoutView(View):
    def get(self, request):
        # Tizimdan chiqish (session'ni o'chirish)
        logout(request)
        # Chiqib ketgandan keyin qayerga o'tishini yozasan (masalan, home sahifasiga)
        return redirect('accounts:login')

    
class ProfileView(View):
    def get(self, request):
        context = {
            'user': request.user
        }
        return render(request, 'accounts/profile.html', context)

class ProfileUpdateView(View):

    def get(self, request):
        form = ProfileForm(instance=request.user)
        return render(request, 'accounts/profile_update.html', {'form': form})

    def post(self, request):

        form = ProfileForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('profile')  
        return render(request, 'accounts/profile_update.html', {'form': form})





class CustomPasswordChangeView(View):
    def get(self, request):
        form = CustomPasswordChangeForm(user=request.user)
        return render(request, 'accounts/password_change.html', {'form': form})

    def post(self, request):
        form = CustomPasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            new_password = form.cleaned_data.get('new_password')
            
            # Yangi parolni o'rnatamiz
            request.user.set_password(new_password)
            request.user.save()
            
            # Parol o'zgarganda user tizimdan chiqib ketmasligi uchun session'ni yangilab qo'yamiz
            update_session_auth_hash(request, request.user)
            
            return redirect('accounts:profile') # Profil sahifasiga qaytaramiz
            
        return render(request, 'accounts/password_change.html', {'form': form})