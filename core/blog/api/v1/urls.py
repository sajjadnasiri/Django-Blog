from django.urls import path
from .views import PostView, CategoryView, TagView

app_name = "api-v1"

urlpatterns = [
    path("categories/", CategoryView.as_view({"get": "list"}), name="categories"),
    path(
        "categories/<int:pk>/",
        CategoryView.as_view(
            {
                "get": "retrieve",
                "put": "update",
                "patch": "partial_update",
                "delete": "destroy",
            }
        ),
        name="category",
    ),
    path("tags/", TagView.as_view({"get": "list"}), name="tags"),
    path(
        "tags/<int:pk>/",
        TagView.as_view(
            {
                "get": "retrieve",
                "put": "update",
                "patch": "partial_update",
                "delete": "destroy",
            }
        ),
        name="tag",
    ),
    path("posts/", PostView.as_view({"get": "list", "post": "create"}), name="posts"),
    path(
        "posts/<int:pk>/",
        PostView.as_view(
            {
                "get": "retrieve",
                "put": "update",
                "patch": "partial_update",
                "delete": "destroy",
            }
        ),
        name="post",
    ),
]
