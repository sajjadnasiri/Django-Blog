from django.urls import path
from .views import SignUpAPIView, VerifyAPIView


urlpatterns =[
    path('signup/', SignUpAPIView.as_view(), name='signup'),
    
]

