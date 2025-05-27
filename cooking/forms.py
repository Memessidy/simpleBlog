from django import forms
from .models import Post
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm


class PostAddForm(forms.ModelForm):
    """Форма для додавання нової статті від користувача"""

    class Meta:
        """мета класс, вказує поведінковий характер, коеслення для классу"""
        model = Post
        fields = ('title', 'content', 'photo', 'category')

        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'content': forms.Textarea(attrs={'class': 'form-control'}),
            'photo': forms.FileInput(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
        }

class LoginForm(AuthenticationForm):
    """Форма для аутентифвкації користувача"""
    username = forms.CharField(
        label="Ім'я користувача",
        max_length=150,
        widget=forms.TextInput(attrs={'class': 'form-control'}))

    password = forms.CharField(
        label="ПАРОЛЬ",
        max_length=150,
        strip=False,
        widget=forms.PasswordInput(attrs={'class': 'form-control'}))
