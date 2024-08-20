from django.urls import path
from .views import PostsListView, PostDetail, CreateView, UpdateView, DeleteView


urlpatterns = [
    path('', PostsListView.as_view()),
    path('<int:pk>/', PostDetail.as_view()),
]