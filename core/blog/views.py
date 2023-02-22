from django.shortcuts import render
from django.views.generic.base import TemplateView
from django.views.generic import DetailView
from .models import Post


class IndexView(TemplateView):
    template_name = "test-template/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["posts"] = Post.objects.all()
        return context


class PostDetailView(DetailView):
    template_name = "test-template/post-list.html"
    queryset = Post.objects.filter(published=True)

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        posts = super().get_context_data(**kwargs)
        return posts
