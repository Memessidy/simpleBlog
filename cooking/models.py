from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
import website_settings


class Category(models.Model):
    """Категорія новин"""
    title = models.CharField(max_length=255, verbose_name='Назва категорії')

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('category_list', kwargs={'pk': self.pk})

    class Meta:
        verbose_name = 'Категорія'
        verbose_name_plural = 'Категорії'


class Post(models.Model):
    """Для постів новин"""
    title = models.CharField(max_length=255, verbose_name='Заголовок статті')
    content = models.TextField(default='Скоро тут буде стаття..', verbose_name='Текст статті')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата створення')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата оновлення')
    photo = models.ImageField(upload_to='photos/', blank=True, null=True, verbose_name='Зображення')
    watched = models.IntegerField(default=0, verbose_name='Перегляди')
    is_published = models.BooleanField(default=website_settings.publish_without_verification, verbose_name='Публікація')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='Категорія', related_name='posts')
    author = models.ForeignKey(User, default=None, null=True, blank=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post_detail', kwargs={'pk': self.pk})

    class Meta:
        verbose_name = 'Пост'
        verbose_name_plural = 'Пости'


class Comment(models.Model):
    """Коментарі до постів"""
    post = models.ForeignKey(Post, on_delete=models.CASCADE, verbose_name='Пост')
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Користувач')
    text = models.TextField(verbose_name='Коментар')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата створення')

    def __str__(self):
        return self.text

    class Meta:
        verbose_name = 'Коментар'
        verbose_name_plural = 'Коментарі'

