
from django_filters import FilterSet
from django import forms
from .models import Post

class PostFilter(FilterSet):

    # date_in = forms.DateField(widget=forms.DateInput(attrs={'placeholder': 'dd/mm/yyyy'}))

   class Meta:
       model = Post
       fields = {
            'title': ['icontains'],
            'author': ['exact'],
            'date_in': ['date__gt'],
       }
