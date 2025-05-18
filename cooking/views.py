from django.shortcuts import render
from .models import Category, Post

def index(request):
    """Для главной страницы"""
    posts = Post.objects.all()
    context = {
        'title': 'Головна сторінка',
        'posts': posts
    }

    return render(request, 'cooking/index.html', context)
