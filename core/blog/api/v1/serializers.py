from rest_framework import serializers
from ...models import Post, Category, Tag
from accounts.models import Profile


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ('id', 'name')


class TagSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Tag
        fields = ('id', 'name')


class PostSerializer(serializers.Serializer):
    pass