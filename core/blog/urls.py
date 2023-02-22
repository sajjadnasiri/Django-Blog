from django.urls import path, include
from .views import IndexView, PostDetailView


app_name = "blog"

urlpatterns = [
    path("index/", IndexView.as_view(), name="index"),
    path("postdetail/<int:pk>/", PostDetailView.as_view(), name="postdetail"),
    path("api/v1/", include("blog.api.v1.urls")),
]
