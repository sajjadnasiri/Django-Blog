from django.urls import path, include


app_name = "accounts"

urlpatterns = [
    path('', include('accounts.api.v1.urls'), name='api-v1'),
]