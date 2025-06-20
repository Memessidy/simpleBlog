from django.shortcuts import render, redirect
from django.db.models import F, Q
from django.contrib.auth import login, logout
from django.contrib import messages
from django.views.generic import ListView, DetailView, CreateView, DeleteView, UpdateView
from django.urls import reverse_lazy
from django.contrib.auth.models import User
from django.contrib.auth.views import PasswordChangeView
from .serializers import PostSerializer, CategorySerializer
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.permissions import IsAuthenticated

from .models import Post, Category, Comment
from .forms import PostAddForm, LoginForm, RegisterForm, CommentForm
import website_settings


# def index(request):
#     """Для главной страницы"""
#     posts = Post.objects.all()
#
#     context = {
#         'title': 'Головна сторінка',
#         'posts': posts,
#     }
#
#     return render(request, 'cooking/index.html', context)

class Index(ListView):
    """Для головної сторінки"""
    model = Post
    context_object_name = 'posts'
    template_name = 'cooking/index.html'
    extra_context = {'title': 'Головна сторінка', 'name': website_settings.website_name}


# def category_list(request, pk):
#     """Реакція на натискання кнопки категорії"""
#     posts = Post.objects.filter(category_id=pk)
#
#     if posts:
#         current_category = posts[0].category.title
#     else:
#         current_category = 'Головна сторінка'
#
#     context = {
#         'title': current_category,
#         'posts': posts,
#     }
#
#     return render(request, 'cooking/index.html', context)


class ArticleByCategory(Index):
    """Реакція на натискання кнопки категорії"""

    def get_queryset(self):
        """Тут можна перероблювати фільтрацію"""
        return Post.objects.filter(category_id=self.kwargs['pk'], is_published=True)

    def get_context_data(self, *, object_list=None, **kwargs):
        """Для динамічних даних"""
        context = super().get_context_data()
        category = Category.objects.get(pk=self.kwargs['pk'])
        context['title'] = category.title
        return context


# def post_detail(request, pk):
#     """Сторінка статті"""
#     article = Post.objects.get(id=pk)
#
#     ext_posts = Post.objects.all().exclude(pk=article.pk)
#     ext_posts = ext_posts.order_by('-watched')[:5]
#
#     Post.objects.filter(pk=pk).update(watched=F('watched') + 1)
#     context = {
#         'title': article.title,
#         'post': article,
#         'ext_posts': ext_posts,
#     }
#
#     return render(request, 'cooking/article_detail.html', context)

class PostDetail(DetailView):
    """Сторінка статті"""
    model = Post
    template_name = 'cooking/article_detail.html'

    def get_queryset(self):
        """Тут можна робити додаткову фільтрацію"""
        return Post.objects.filter(pk=self.kwargs['pk'])

    def get_context_data(self, **kwargs):
        """Для динамічних даних"""
        context = super().get_context_data()
        Post.objects.filter(pk=self.kwargs['pk']).update(watched=F('watched') + 1)
        post = Post.objects.get(id=self.kwargs['pk'])
        ext_posts = Post.objects.all().exclude(pk=post.pk)
        ext_posts = ext_posts.order_by('-watched')[:5]
        context['title'] = post.title
        context['ext_posts'] = ext_posts
        context['comments'] = Comment.objects.filter(post=post)

        if self.request.user.is_authenticated:
            context['comment_form'] = CommentForm
        return context


# def add_post(request):
#     """Додавання статті від користувача, без адмінки"""
#     if request.method == 'POST':
#         form = PostAddForm(request.POST, request.FILES)
#         if form.is_valid():
#             post = Post.objects.create(**form.cleaned_data)
#             post.save()
#             return redirect('post_detail', pk=post.pk)
#     else:
#         form = PostAddForm()
#
#         context = {
#             'form': form,
#             'title': 'Додати статтю'
#         }
#         return render(request, 'cooking/article_add_form.html', context)

class AddPost(CreateView):
    """Додавання статті від користувача, без адмінки"""
    form_class = PostAddForm
    template_name = 'cooking/article_add_form.html'
    extra_context = {'title': 'Додати статтю'}

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class SearchResult(Index):
    """Пошук слова в заголовках і в змісту статей"""

    def get_queryset(self):
        """Функція для фільтрації вибірок із db"""
        word = self.request.GET.get('q')
        posts = Post.objects.filter(
            Q(title__icontains=word) | Q(content__icontains=word)
        )
        return posts


class PostUpdate(UpdateView):
    """Зміна статті по кнопці"""
    model = Post
    form_class = PostAddForm
    template_name = 'cooking/article_add_form.html'


class PostDelete(DeleteView):
    """Видалення статті по кнопці"""
    model = Post
    success_url = reverse_lazy('index')
    context_object_name = 'post'
    extra_context = {'title': 'Змінити статтю'}


def add_comment(request, post_id):
    """Додавання коментарів до статей"""
    form = CommentForm(request.POST)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.user = request.user
        comment.post = Post.objects.get(pk=post_id)
        comment.save()
        messages.success(request, 'Ваш коментар успішно додано!')

    return redirect('post_detail', pk=post_id)


def user_login(request):
    """Аутентифікація користувача"""
    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, message='Ви успішно зайшли в аккаунт!')
            return redirect('index')
        else:
            context = {
                'title': 'Авторизація користувача',
                'form': form
            }
            return render(request, 'cooking/login_form.html', context)
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


def register(request):
    """Реєстрація користувача"""
    if request.method == 'POST':
        form = RegisterForm(data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = RegisterForm()

    context = {
        'title': 'Реєстрація користувача',
        'form': form
    }

    return render(request, 'cooking/register.html', context)


def profile(request, user_id):
    """Сторінка користувача"""
    user = User.objects.get(pk=user_id)
    posts = Post.objects.filter(author=user)
    context = {
        'user': user,
        'posts': posts,
    }
    return render(request, 'cooking/profile.html', context)


class UserChangePassword(PasswordChangeView):
    template_name = 'cooking/change_password.html'
    """Простий спосіб зміни пароля користувача"""
    success_url = reverse_lazy('index')


class CookingApi(ListAPIView):
    """Видача усіх статей по API"""
    queryset = Post.objects.filter(is_published=True)
    serializer_class = PostSerializer


class CookingApiDetail(RetrieveAPIView):
    """Видача статей по API"""
    queryset = Post.objects.filter(is_published=True)
    serializer_class = PostSerializer
    permission_classes = (IsAuthenticated,)


class CategoryApi(ListAPIView):
    """Видача усіх категорій по API"""
    queryset = Post.objects.filter(is_published=True)
    serializer_class = PostSerializer

class CategoryApiDetail(RetrieveAPIView):
    """Видача усіх по API"""
    queryset = Post.objects.filter(is_published=True)
    serializer_class = CategorySerializer
    permission_classes = (IsAuthenticated,)

