from django.shortcuts import render
from django.views.generic import ListView, DetailView
from blog.models import Post

# Create your views here.
class PostListView(ListView):
    model = Post
    template_name = 'blog/postList.html'
    context_object_name = 'postList'
    ordering = ['-published_at']

class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/postDetail.html'
    context_object_name = 'postDetail'