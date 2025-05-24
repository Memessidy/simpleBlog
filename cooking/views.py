from django.shortcuts import render
from .models import Post
from django.db.models import F

def index(request):
    """Для главной страницы"""
    posts = Post.objects.all()

    context = {
        'title': 'Головна сторінка',
        'posts': posts,
    }

    return render(request, 'cooking/index.html', context)


def category_list(request, pk):
    """Реакція на натискання кнопки категорії"""
    posts = Post.objects.filter(category_id=pk)

    if posts:
        current_category= posts[0].category.title
    else:
        current_category = 'Головна сторінка'

    context = {
        'title': current_category,
        'posts': posts,
    }

    return render(request, 'cooking/index.html', context)


def post_detail(request, pk):
    """Сторінка статті"""
    article = Post.objects.get(id=pk)

    ext_posts = Post.objects.all().exclude(pk=article.pk)
    ext_posts = ext_posts.order_by('-watched')[:5]

    Post.objects.filter(pk=pk).update(watched=F('watched') + 1)
    context = {
        'title': article.title,
        'post': article,
        'ext_posts': ext_posts,
    }

    return render(request, 'cooking/article_detail.html', context)
