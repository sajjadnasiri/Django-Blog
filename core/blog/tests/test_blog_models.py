from datetime import datetime
from django.test import TestCase
from ..models import Post, Category, Tag
from accounts.models import User, Profile
from faker import Faker


fake = Faker()


class TestModels(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email="test@test.com", password="!@#jkJK9cd34"
        )
        self.profile = Profile.objects.get(user=self.user)
        self.category = Category.objects.create(name="Test")
        self.tag = Tag.objects.create(name="Test")

    def test_post_model(self):
        post = Post.objects.create(
            author=self.profile,
            title="test",
            description=fake.text(),
            content=fake.text(1024 * 2),
            published=True,
            view=0,
            published_date=datetime.now(),
        )
        post.category.add(self.category)
        post.tag.add(self.tag)
        self.assertTrue(Post.objects.filter(pk=post.id).exists())
