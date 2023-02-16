from django_filters import rest_framework as filters
from blog.models import Post


class PostFilters(filters.FilterSet):

    class Meta:
        model = Post
        fields = {
            "author": ["in"],
            "title": ["exact", "in"],
        }

