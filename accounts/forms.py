from django import forms
from .models import CustomUser
from django.core.exceptions import ValidationError
from django.contrib.auth.password_validation import validate_password


class CustomUserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'PASSWORD', 'class': 'box'}))
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'CONFIRM PASSWORD', 'class': 'box'}))

    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'username', 'email', 'password']
        widgets = {
            'first_name': forms.TextInput(attrs={'placeholder': 'FIRST NAME', 'class': 'box'}),
            'last_name': forms.TextInput(attrs={'placeholder': 'LAST NAME', 'class': 'box'}),
            'email': forms.EmailInput(attrs={'placeholder': 'EMAIL', 'class': 'box'}),
            'username': forms.TextInput(attrs={'placeholder': 'USERNAME', 'class': 'box'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        
        if password:
            if len(password) < 8:
                raise ValidationError("Parol kamida 8 ta belgidan iborat bo'lishi kerak.")

            if not any(char.isalpha() for char in password):
                raise ValidationError('Parolda kamida bitta harf qatnashsin')
            
            if not any(char.isdigit() for char in password):
                raise ValidationError("Parolda kamida bitta raqam qatnashishi kerak.")

            special_characters = '!@#$%&+-=/'
            if not any(char in special_characters for char in password):
                raise ValidationError("Parolda kamida bitta maxsus belgi bo'lsin: !@#$%&+-=/ ")

        
        if password and confirm_password and password != confirm_password:
            raise ValidationError("Parollar bir-biriga mos emas.")

        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False) 
        user.set_password(self.cleaned_data['password']) 
        if commit:
            user.save()
        return user


class LoginForm(forms.Form):
    username = forms.CharField(
        max_length=150,
        widget=forms.TextInput(attrs={'placeholder': 'Username kiriting'}),
        label="Username"
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Parol kiriting'}),
        label="Parol"
    )

class ProfileForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        # Faqat ruxsat etilgan maydonlarni yozamiz:
        fields = ['avatar', 'first_name', 'last_name', 'username', 'email', 'bio', 'social_links', 'websites']
        widgets = {
            'first_name': forms.TextInput(attrs={'placeholder': 'FIRST NAME', 'class': 'box'}),
            'last_name': forms.TextInput(attrs={'placeholder': 'LAST NAME', 'class': 'box'}),
            'username': forms.TextInput(attrs={'placeholder': 'USERNAME', 'class': 'box'}),
            'email': forms.EmailInput(attrs={'placeholder': 'EMAIL', 'class': 'box'}),
            'bio': forms.TextInput(attrs={'placeholder': 'BIO', 'class': 'box'}),
            'social_links': forms.URLInput(attrs={'placeholder': 'https://t.me/username', 'class': 'box'}),
            'websites': forms.URLInput(attrs={'placeholder': 'https://example.com', 'class': 'box'}),
        }

class ProfileForm(forms.ModelForm):

    class Meta:
        model = CustomUser
        fields = ['avatar', 'first_name', 'last_name', 'username', 'email', 'bio', 'social_links', 'websites']
        widgets = {
            'first_name': forms.TextInput(attrs={'placeholder': 'FIRST NAME', 'class': 'box'}),
            'last_name': forms.TextInput(attrs={'placeholder': 'LAST NAME', 'class': 'box'}),
            'username': forms.TextInput(attrs={'placeholder': 'USERNAME', 'class': 'box'}),
            'email': forms.EmailInput(attrs={'placeholder': 'EMAIL', 'class': 'box'}),
            'bio': forms.TextInput(attrs={'placeholder': 'BIO', 'class': 'box'}),
            'social_links': forms.TextInput(attrs={'placeholder': 't.me/username yoki https://t.me/...', 'class': 'box'}), # URLInput o'rniga TextInput qildik
            'websites': forms.TextInput(attrs={'placeholder': 'kun.uz yoki https://kun.uz', 'class': 'box'}),
        }

    def clean_social_links(self):
        url = self.cleaned_data.get('social_links')
        if url and not url.startswith(('http://', 'https://')):
            url = 'https://' + url
        return url

    def clean_websites(self):
        url = self.cleaned_data.get('websites')
        if url and not url.startswith(('http://', 'https://')):
            url = 'https://' + url
        return url





class CustomPasswordChangeForm(forms.Form):
    old_password = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Eski parol', 'class': 'box'}),
        label="Eski parol"
    )
    new_password = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Yangi parol', 'class': 'box'}),
        label="Yangi parol"
    )
    confirm_new_password = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Yangi parolni tasdiqlang', 'class': 'box'}),
        label="Yangi parolni tasdiqlash"
    )

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super().__init__(*args, **kwargs)

    def clean_old_password(self):
        old_password = self.cleaned_data.get('old_password')
        # Eski parol to'g'riligini tekshiramiz
        if not self.user.check_password(old_password):
            raise forms.ValidationError("Eski parol xato kiritildi.")
        return old_password

    def clean(self):
        cleaned_data = super().clean()
        new_password = cleaned_data.get('new_password')
        confirm_new_password = cleaned_data.get('confirm_new_password')

        if new_password and confirm_new_password:
            if new_password != confirm_new_password:
                raise forms.ValidationError("Yangi parollar bir-biriga mos kelmadi.")
            
            # Django'ning o'ning kuchli parol talablarini tekshiruvidan o'tkazish
            try:
                validate_password(new_password, self.user)
            except forms.ValidationError as e:
                self.add_error('new_password', e)

        return cleaned_data