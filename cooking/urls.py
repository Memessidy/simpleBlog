from django.urls import path
from . import views
from .views import add_post

urlpatterns = [
    path('', views.index, name='index'),
    path('category/<int:pk>/', views.category_list, name='category_list'),
    path('post/<int:pk>/', views.post_detail, name='post_detail'),
    path('add_article/', add_post, name='add'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('register/', views.register, name='register'),

]
