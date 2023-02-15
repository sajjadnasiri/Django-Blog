from django.db import models
from accounts.models import Profile

# Create your models here.
class Post(models.Model):
    title = models.CharField(max_length=255)
    description = models.CharField(max_length=1024*2, blank=True)
    content = models.TextField(blank=True)
    published = models.BooleanField(default=False)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)
    published_date = models.DateTimeField(blank=True, null=True)
    view = models.IntegerField(default=0)

    author = models.ForeignKey(Profile, on_delete=models.PROTECT)
    category = models.ManyToManyField("Category")
    tag = models.ManyToManyField("Tag")

    class Meta:
        ordering = ["-published_date", "-created_date"]

    def __str__(self):
        return self.title


# Tag
class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


# Category
class Category(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name