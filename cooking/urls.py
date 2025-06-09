from django.urls import path
from . import views

urlpatterns = [
    # Classes
    # path('', views.index, name='index'),
    path('', views.Index.as_view(), name='index'),
    # path('category/<int:pk>/', views.category_list, name='category_list'),
    path('category/<int:pk>/', views.ArticleByCategory.as_view(), name='category_list'),
    # path('post/<int:pk>/', views.post_detail, name='post_detail'),
    path('post/<int:pk>/', views.PostDetail.as_view(), name='post_detail'),
    # path('add_article/', views.add_post, name='add'),
    path('add_article/', views.AddPost.as_view(), name='add'),
    path('post/<int:pk>/update/', views.PostUpdate.as_view(), name='post_update'),
    path('post/<int:pk>/delete/', views.PostDelete.as_view(), name='post_delete'),
    path('search/', views.SearchResult.as_view(), name='search'),


    # Functions
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('register/', views.register, name='register'),

]
