from django import template
from cooking.models import Category
from django.db.models import Count
from django.db.models import Q
import website_settings

register = template.Library()


@register.simple_tag()
def get_all_categories():
    """Кнопки категорий"""
    # return Category.objects.annotate(cnt=Count('posts')).filter(cnt__gt=0)
    return Category.objects.annotate(cnt=Count(
        'posts', filter=Q(posts__is_published=True))).filter(cnt__gt=0)


@register.simple_tag()
def get_footer_text():
    """Текст футера"""
    return website_settings.footer_text

