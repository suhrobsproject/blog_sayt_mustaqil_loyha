from django.urls import path
from .views import (
    RegisterView, LoginView, home, ProfileUpdateView, 
    ProfileView, CustomPasswordChangeView, CustomLogoutView,
    UserProfileDetailView  # Yangi view
)

app_name = 'accounts'

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('user/<str:username>/', UserProfileDetailView.as_view(), name='user-profile'), # Yangi URL
    path('profile_update/', ProfileUpdateView.as_view(), name='profile_update'),
    path('password-change/', CustomPasswordChangeView.as_view(), name='password_change'),
    path('logout/', CustomLogoutView.as_view(), name='logout'),
    path('', home, name='home')
]