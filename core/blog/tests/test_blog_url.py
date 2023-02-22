from django.test import SimpleTestCase, TestCase
from django.urls import reverse, resolve
from ..views import IndexView, PostDetailView


class TestUrl(TestCase):
    def test_blog_index_url(self):
        url = reverse("blog:index")
        self.assertEquals(resolve(url).func.view_class, IndexView)

    def test_blog_posts_url(self):
        url = reverse("blog:postdetail", kwargs={"pk": 220})
        self.assertEqual(resolve(url).func.view_class, PostDetailView)
