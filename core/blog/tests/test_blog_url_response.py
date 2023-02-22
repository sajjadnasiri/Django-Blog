from datetime import datetime
from django.test import TestCase
from django.urls import reverse, resolve
from ..models import Post
from accounts.models import User, Profile


class TestResponse(TestCase):
    def setUp(self) -> None:
        self.user = User.objects.create_user(
            email="test@test.com", password="!@23sdc23Cks"
        )
        self.profile = Profile.objects.get(id=self.user.id)
        self.post = Post.objects.create(
            author=self.profile,
            title="test",
            description="test description",
            content="test content",
            published=True,
            published_date=datetime.now(),
        )
        return super().setUp()

    def test_index_url_response(self):
        url = reverse("blog:index")
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)
        self.assertTrue(str(response.content).find("index"))
        self.assertTemplateUsed(response, template_name="test-template/index.html")

    def test_detial_url_response(self):
        url = reverse("blog:postdetail", kwargs={"pk": self.post.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.reason_phrase, "OK")
        self.assertTrue(response.closed)
        self.assertTrue(str(response.content).find("postdetail"))
        self.assertTemplateUsed(response, template_name="test-template/post-list.html")

    def test_detial_url_response_anonymouse(self):
        url = reverse("blog:postdetail", kwargs={"pk": self.post.id + 1})
        response = self.client.get(url)
        self.assertTrue(response.status_code, 404)
