from django.shortcuts import render, redirect
from .models import Post
from django.db.models import F
from .forms import PostAddForm, LoginForm
from django.contrib.auth import login, logout


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
        current_category = posts[0].category.title
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


def add_post(request):
    """Додавання статті від користувача, без адмінки"""
    if request.method == 'POST':
        form = PostAddForm(request.POST, request.FILES)
        if form.is_valid():
            post = Post.objects.create(**form.cleaned_data)
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostAddForm()

        context = {
            'form': form,
            'title': 'Додати статтю'
        }
        return render(request, 'cooking/article_add_form.html', context)


def user_login(request):
    """Аутентифікація користувача"""
    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('index')
    else:
        form = LoginForm()

        context = {
            'title': 'Авторизація користувача',
            'form': form
        }
        return render(request, 'cooking/login_form.html', context)


def user_logout(request):
    """Вихід користувача"""
    logout(request)
    return redirect('index')

