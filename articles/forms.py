from django import forms
from .models import Article, Tag, Comment

class ArticleForm(forms.ModelForm):
    tags = forms.ModelMultipleChoiceField(
        queryset=Tag.objects.all(),
        required=False,
        widget=forms.CheckboxSelectMultiple(attrs={'class': 'btn-check'}),
        label="Teglar"
    )
    image = forms.ImageField(
        required=False,
        widget=forms.FileInput(attrs={'class': 'form-control', 'accept': 'image/*'}),
        label="Muqova rasmi (Kompyuterdan tanlang)"
    )

    class Meta:
        model = Article
        fields = ['category', 'title', 'image', 'description', 'article', 'tags']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Masalan: Django REST Framework bilan ishlash'}),
            'category': forms.Select(attrs={'class': 'form-select'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'Maqolaning qisqacha mazmuni'}),
            'article': forms.Textarea(attrs={'class': 'form-control font-monospace', 'rows': 9, 'placeholder': 'Maqola matni va kod bloklari...'}),
        }


class CommentForm(forms.ModelForm):
    parent_id = forms.IntegerField(widget=forms.HiddenInput(), required=False)

    class Meta:
        model = Comment
        fields = ['comment']
        widgets = {
            'comment': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Fikringizni yozing yoki kod yechimlarini ulashing...'
            })
        }