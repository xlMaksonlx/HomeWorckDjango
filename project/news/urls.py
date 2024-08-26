from django.urls import path
from .views import PostsListView, PostDetail, PostCreate, PostUpdate, PostDelete


urlpatterns = [
    path('', PostsListView.as_view(), name='posts_list'),
    path('<int:pk>/', PostDetail.as_view()),
    path('news/create/', PostCreate.as_view(), name='news_create'),
    path('articles/create/', PostCreate.as_view(), name='articles_create'),
    path('news/<int:pk>/update', PostUpdate.as_view()),
    path('news/<int:pk>/delete', PostDelete.as_view()),
    path('articles/<int:pk>/update', PostUpdate.as_view()),
    path('articles/<int:pk>/delete', PostDelete.as_view()),
]