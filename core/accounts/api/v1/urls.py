from django.urls import path
from .views import (SignUpAPIView, TokeObtainAPIView, TokenDiscardAPIView, CustomTokenObtainPairView,
                    ChangePasswordAPIView, ActivationConfirmView, ProfileAPIView)


app_name = "api-v1"

urlpatterns =[
    path('signup/', SignUpAPIView.as_view(), name='signup'),
    path('token/login/', TokeObtainAPIView.as_view(), name='obtain-token'),
    path('token/logout/', TokenDiscardAPIView.as_view(), name='discard-token'),

    path('jwt/createtoken/', CustomTokenObtainPairView.as_view(), name="jwt-create"),
    path('jwt/changepassword/', ChangePasswordAPIView.as_view(), name="change-password"),

    path('jwt/activation/<str:jwt_token>', ActivationConfirmView.as_view(), name="acivation"),
    
    path('profile/', ProfileAPIView.as_view(), name="profile"),
]
