from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum
from django.db.models.functions import Coalesce
from django.urls import reverse


class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    rating = models.IntegerField(null=True)

    def update_rating(self):
        post_rating = self.posts.aggregate(pr=Coalesce(Sum('rating'), 0)).get('pr')
        comments_rating = self.user.comments.aggregate(cr=Coalesce(Sum('rating'), 0))['cr']
        posts_comment_rating = self.posts.aggregate(pcr=Coalesce(Sum('comment__rating'),0))['pcr']

        self.rating = post_rating * 3 + comments_rating + posts_comment_rating
        self.save()

    def __str__(self):
        return self.user.username




class Category(models.Model):
    name = models.CharField(max_length=50, unique=True)
    def __str__(self):
        return self.name


class Post(models.Model):
    article = 'AR'
    news = 'NE'

    POSITIONS =[
        (article, 'article'),
        (news, 'news'),
    ]

    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='posts')
    news_art = models.CharField(max_length=2,choices=POSITIONS,default='NE')
    date_in = models.DateTimeField(auto_now_add=True)
    category = models.ManyToManyField(Category, through='PostCategory')
    title = models.CharField(max_length=255)
    text = models.TextField(default='')
    rating = models.IntegerField(default=0)

    def like(self):
        self.rating+=1
        self.save()
        return self.rating

    def dislike(self):
        self.rating-=1
        self.save()
        return self.rating

    def preview(self):
        if len(self.text) > 20:
            return f'{self.text[:20]} ...'
        else:
            return f'{self.text[:len(self.text)]}'

    def __str__(self):
        return f'{self.title}: {self.text}'

    def get_absolute_url(self):
        return reverse('post_detail', args=[str(self.id)])


class PostCategory(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)



class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    text = models.TextField(default='')
    date_in = models.DateTimeField(auto_now_add=True)
    rating = models.IntegerField(default=0)

    def like(self):
        self.rating+=1
        self.save()
        return self.rating

    def dislike(self):
        self.rating-=1
        self.save()
        return self.rating



