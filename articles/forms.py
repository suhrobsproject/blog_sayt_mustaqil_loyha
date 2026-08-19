from django import forms
from .models import Article

class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ['category', 'title', 'image', 'description', 'article', 'slug']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Maqola sarlavhasi'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'image': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Rasm havolasi (URL)'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Qisqacha tavsif'}),
            'article': forms.Textarea(attrs={'class': 'form-control', 'rows': 6, 'placeholder': 'Maqola matni'}),
            'slug': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'url-slug-nomi'}),
        }