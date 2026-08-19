from django import forms
from django.contrib.auth.password_validation import validate_password
from .models import CustomUser

class CustomUserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Parol', 'class': 'form-control'}))
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Parolni tasdiqlang', 'class': 'form-control'}))

    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'username', 'email', 'password']
        widgets = {
            'first_name': forms.TextInput(attrs={'placeholder': 'Ism', 'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'placeholder': 'Familiya', 'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'placeholder': 'Email', 'class': 'form-control'}),
            'username': forms.TextInput(attrs={'placeholder': 'Username', 'class': 'form-control'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password and confirm_password and password != confirm_password:
            self.add_error('confirm_password', "Parollar bir-biriga mos kelmadi.")
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
        widget=forms.TextInput(attrs={'placeholder': 'Username kiriting', 'class': 'form-control'}),
        label="Username"
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Parol kiriting', 'class': 'form-control'}),
        label="Parol"
    )


class ProfileForm(forms.ModelForm):
    avatar = forms.ImageField(
        required=False, 
        widget=forms.FileInput(attrs={'class': 'form-control', 'accept': 'image/*'})
    )

    class Meta:
        model = CustomUser
        fields = ['avatar', 'first_name', 'last_name', 'username', 'email', 'bio', 'social', 'websites']
        widgets = {
            'first_name': forms.TextInput(attrs={'placeholder': 'Ism', 'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'placeholder': 'Familiya', 'class': 'form-control'}),
            'username': forms.TextInput(attrs={'placeholder': 'Username', 'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'placeholder': 'Email', 'class': 'form-control'}),
            'bio': forms.Textarea(attrs={'placeholder': 'Masalan: Python backend dasturchi | Django & FastAPI...', 'class': 'form-control', 'rows': 3}),
            'social': forms.TextInput(attrs={'placeholder': 'https://t.me/username yoki https://github.com/...', 'class': 'form-control'}),
            'websites': forms.TextInput(attrs={'placeholder': 'https://mysite.uz', 'class': 'form-control'}),
        }

    def clean_social(self):
        url = self.cleaned_data.get('social')
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
        widget=forms.PasswordInput(attrs={'placeholder': 'Eski parol', 'class': 'form-control'}),
        label="Eski parol"
    )
    new_password = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Yangi parol', 'class': 'form-control'}),
        label="Yangi parol"
    )
    confirm_new_password = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Yangi parolni tasdiqlang', 'class': 'form-control'}),
        label="Yangi parolni tasdiqlash"
    )

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super().__init__(*args, **kwargs)

    def clean_old_password(self):
        old_password = self.cleaned_data.get('old_password')
        if not self.user.check_password(old_password):
            raise forms.ValidationError("Eski parol noto'g'ri kiritildi.")
        return old_password

    def clean(self):
        cleaned_data = super().clean()
        new_password = cleaned_data.get('new_password')
        confirm_new_password = cleaned_data.get('confirm_new_password')

        if new_password and confirm_new_password:
            if new_password != confirm_new_password:
                self.add_error('confirm_new_password', "Yangi parollar bir-biriga mos kelmadi.")
            try:
                validate_password(new_password, self.user)
            except forms.ValidationError as error:
                self.add_error('new_password', error)
        return cleaned_data