from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework import status
from .serializers import PostSerializer, CategorySerializer, TagSerializer
from ...models import Post, Category, Tag


class CategoryView(viewsets.ModelViewSet):
    serializer_class = CategorySerializer
    queryset = Category.objects.all()
    permission_classes = []


class TagView(viewsets.ModelViewSet):
    serializer_class = TagSerializer
    queryset = Tag.objects.all()


