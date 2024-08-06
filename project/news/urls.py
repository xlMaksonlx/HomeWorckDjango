from django.urls import path
from .views import PostsListView, PostDetail


urlpatterns = [
    path('', PostsListView.as_view()),
    path('<int:pk>/', PostDetail.as_view()),
]