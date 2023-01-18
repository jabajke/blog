from django.urls import path
from . import views


urlpatterns = [
    path('', views.news_home, name='news_home'),
    path('create/', views.ArticleCreateView.as_view(), name='create'),
    path('<int:pk>/', views.NewsDetailView.as_view(), name='detail_news'),
    path('<int:pk>/update/', views.NewsUpdateView.as_view(), name='update_news'),
    path('<int:pk>/delete/', views.NewsDeleteView.as_view(), name='delete_news'),
    path('<int:pk>/comment/', views.CommentCreateView.as_view(), name='comment_create')
]
