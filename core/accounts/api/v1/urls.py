from django.urls import path
from .views import SignUpAPIView


app_name = "api-v1"

urlpatterns =[
    path('signup/', SignUpAPIView.as_view(), name='signup'),
    
]

