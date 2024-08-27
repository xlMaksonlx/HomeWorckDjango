from datetime import datetime

from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .filters import PostFilter
from .forms import PostForm
from .models import Post
from django.urls import reverse_lazy


class PostsListView(ListView):
    model = Post
    ordering = '-date_in'
    template_name = 'posts.html'
    context_object_name = 'posts'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = PostFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['time_now'] = datetime.utcnow()
        context['filterset'] = self.filterset
        return context





class PostDetail(DetailView):
    model = Post
    template_name = 'post.html'
    context_object_name = 'post'


class PostCreate(CreateView):
    form_class = PostForm
    model = Post
    template_name = 'post_edit.html'

    def form_valid(self, form):
        post = form.save(commit=False)
        if self.request.path == '/post/articles/create/':
            post.news_art = 'AR'
        elif self.request.path == '/post/news/create/':
            post.news_art = 'NE'
        post.save()
        return super().form_valid(form)


class PostUpdate(UpdateView):
    form_class = PostForm
    model = Post
    template_name = 'post_edit.html'

    def dispatch(self, request, *args, **kwargs):
        post = self.get_object()

        context = {'post_id': post.pk}
        if self.request.path == f'/post/news/{post.pk}/edit/' and post.news_art != 'NE':
            return render(self.request, 'invalid_articles_edit.html', context=context)
        elif self.request.path == f'/post/articles/{post.pk}/edit/' and post.news_art != 'AR':
            return render(self.request, 'invalid_news_edit.html', context=context)
        return super(PostUpdate, self).dispatch(request, *args, **kwargs)



class PostDelete(DeleteView):
    model = Post
    template_name = 'post_delete.html'
    success_url = reverse_lazy('posts_list')

    # def dispatch(self, request, *args, **kwargs):
    #     post = self.get_object()
    #
    #     context = {'post_id': post.pk}
    #     if self.request.path == f'/post/news/{post.pk}/delete/' and post.news_art != 'NE':
    #         return render(self.request, 'invalid_articles_edit.html', context=context)
    #     elif self.request.path == f'/post/articles/{post.pk}/delete/' and post.news_art != 'AR':
    #         return render(self.request, 'invalid_news_edit.html', context=context)
    #     return super(PostUpdate, self).dispatch(request, *args, **kwargs)


