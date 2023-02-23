import pytest
from rest_framework.test import APIClient
from django.urls import reverse
from datetime import datetime
from accounts.models import User, Profile
from ..models import Category, Tag


@pytest.fixture
def api_client():
    client = APIClient()
    return client


@pytest.fixture
def create_user():
    user = User.objects.create_user(
        email="s@nasiri.com", password="sdv@#$Rvsd3", is_verified=True
    )
    # profile = Profile.objects.get(user=user)
    return user


@pytest.fixture
def create_category_tag():
    category = Category.objects.create(name="Category_Test")
    tag = Tag.objects.create(name="Tag_Test")
    return category, tag


@pytest.mark.django_db
class TestResponses:
    def test_200_ok_response(self, api_client):
        url = reverse("blog:api-v1:posts")
        response = api_client.get(url)
        assert response.status_code == 200

    def test_create_post_401(self, api_client):
        # Not Login
        url = reverse("blog:api-v1:posts")
        data = {
            "title": "test",
            "description": "test description",
            "content": "test content",
            "published": True,
            "published_date": datetime.now(),
        }
        response = api_client.post(url, data=data)
        assert response.status_code == 401

    def test_create_post_201(self, api_client, create_user, create_category_tag):
        url = reverse("blog:api-v1:posts")
        category, tag = create_category_tag
        data = {
            "title": "test",
            "published": True,
            "published_date": datetime.now(),
            "category": category.id,
            "tag": tag.id,
        }
        user = create_user
        api_client.force_login(user=user)
        response = api_client.post(url, data=data)
        assert response.status_code == 201

    def test_create_invalid_post_400(
        self, api_client, create_user, create_category_tag
    ):
        url = reverse("blog:api-v1:posts")
        category, tag = create_category_tag
        data = {
            "title": "test",
            "published": True,
            "published_date": datetime.now(),
        }
        user = create_user
        api_client.force_login(user=user)
        response = api_client.post(url, data=data)
        assert response.status_code == 400

"""'scs'dc'sdc'sdc'sdc'sdc'"""