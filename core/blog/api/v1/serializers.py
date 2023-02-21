# vscode rest_framework error -> Ctrl+Shift+P and set it
from rest_framework import serializers
from ...models import Post, Category, Tag
from accounts.models import Profile


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ("id", "name")


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ("id", "name")


class PostSerializer(serializers.ModelSerializer):
    abstract = serializers.SerializerMethodField(method_name="get_snippet")
    post_url = serializers.SerializerMethodField(method_name="get_absolute_url")

    class Meta:
        model = Post
        fields = [
            "id",
            "title",
            "author",
            "category",
            "tag",
            "description",
            "content",
            "abstract",
            "post_url",
            "created_date",
            "published",
        ]
        read_only_fields = ["author", "snippet"]

    def to_representation(self, instance):
        request = self.context.get("request")
        rep = super().to_representation(instance)
        rep["category"] = CategorySerializer(
            instance.category, context={"request": request}, many=True
        ).data
        if request.parser_context.get("kwargs").get("pk"):
            rep.pop("abstract", None)
            rep.pop("post_url", None)
        else:
            rep.pop("description", None)
            rep.pop("content", None)
        return rep

    def get_snippet(self, instance):
        snippets = {}
        snippets["description"] = instance.description[:50] + "..."
        snippets["content"] = instance.description[: 50 * 2] + "..."
        return snippets

    def get_absolute_url(self, obj):
        request = self.context.get("request")
        return request.build_absolute_uri(obj.pk)

    def create(self, validated_data):
        validated_data["author"] = Profile.objects.get(
            user__id=self.context.get("request").user.id
        )
        return super().create(validated_data)
