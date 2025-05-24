from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('category/<int:pk>/', views.category_list, name='category_list'),
    path('post/<int:pk>/', views.post_detail, name='post_detail'),

]
