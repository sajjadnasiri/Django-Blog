from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Profile


admin.site.register(Profile)

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    model = User
    list_display = ["email", "is_superuser", "is_staff", "is_verified", "is_active", "created_date"]
    list_filter = ["is_superuser", "is_staff", "is_verified", "is_active"]
    searching_fields = ["email"]
    ordering = ["-created_date"]
    list_editable = ["is_active"]

    fieldsets = (
        (
            "Authentication",
            {
                "fields": ("email", "password")
            }
        ),
        (
            "Permissions",
            {
                "fields": ("is_superuser", "is_staff", "is_verified", "is_active")
            }
        ),
        (
            "Group Permissions",
            {
                "fields": ("groups", "user_permissions")
            }
        ),
        (
            "important date",
            {
                "fields": ("last_login",)
            }
        ),
    )

    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide"),
                "fields": (
                    "email",
                    "password1",
                    "password2",
                    "is_staff",
                    "is_active",
                    "is_superuser",
                    "is_verified",
                ),
            }
        ),
    )