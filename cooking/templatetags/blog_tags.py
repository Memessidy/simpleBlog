from django import template
from cooking.models import Category

register = template.Library()


@register.simple_tag()
def get_all_categories():
    """Кнопки категорий"""
    return Category.objects.all()

@register.simple_tag()
def get_footer_text():
    """Текст футера"""
    return "LinkinSimpsonForever"
