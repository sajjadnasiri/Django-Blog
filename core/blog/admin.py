from django.contrib import admin
from .models import Post, Category, Tag


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ["title", "author", "published", "published_date", "created_date"]
    list_editable = ["published"]
    search_fields = ["title"]
    list_filter = ["author", "published"]
    date_hierarchy = "created_date"


admin.site.register(Category)
admin.site.register(Tag)
