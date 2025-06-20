from django.urls import path
from rest_framework_simplejwt import views as jwt_views

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
    path('password/', views.UserChangePassword.as_view(), name='change_password'),

    # Functions
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('register/', views.register, name='register'),
    path('add_comment/<int:post_id>/', views.add_comment, name='add_comment'),
    path('profile/<int:user_id>/', views.profile, name='profile'),

    # API
    path('api/token/', jwt_views.TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/verify/', jwt_views.TokenVerifyView.as_view(), name='token_verify'),
    path('posts/api/', views.CookingApi.as_view(), name='CookingApi'),
    path('posts/api/<int:pk>/', views.CookingApiDetail.as_view(), name='CookingApiDetail'),
    path('categories/api/', views.CategoryApi.as_view(), name='CookingCategory'),
    path('categories/api/<int:pk>/', views.CategoryApiDetail.as_view(), name='CookingCategoryDetail'),

]
