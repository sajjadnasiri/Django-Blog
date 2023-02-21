from django.conf import settings
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView
from jwt.exceptions import ExpiredSignatureError, InvalidSignatureError
import jwt
from mail_templated import EmailMessage
from ..util import SendMail
from .serializers import (
    SignUpSerializer,
    CustomObtainTokenSerializer,
    CustomTokenObtainPairSerializer,
    ChangePasswordSerializer,
    ProfileSerializer,
)
from ...models import User, Profile


class SignUpAPIView(generics.GenericAPIView):
    serializer_class = SignUpSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            serializer.save()
            email = serializer.validated_data["email"]
            user_object = get_object_or_404(User, email=email)
            token = self.token_generator(user_object)
            email_context = EmailMessage(
                "email/activation.tpl",
                {"Click here": token},
                "admin@admin.com",
                to=[email],
            )
            SendMail(email_context).start()
            detail = {
                "details": email + " created successfully",
                "Click here to verify your profile": "http://127.0.0.1:8000/" + token,
            }
            return Response(detail, status=status.HTTP_201_CREATED)
        return Response({"details": "Bad request"}, status=status.HTTP_400_BAD_REQUEST)

    def token_generator(self, user):
        refresh = RefreshToken.for_user(user)
        return str(refresh.access_token)


class TokeObtainAPIView(ObtainAuthToken):
    serializer_class = CustomObtainTokenSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(
            data=request.data, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        token, created = Token.objects.get_or_create(user=user)
        return Response({"token": token.key, "user": user.pk, "email": user.email})


class TokenDiscardAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        request.user.auth_token.delete()
        return Response(
            {"Details": "token deleted successfully"}, status=status.HTTP_200_OK
        )


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


class ChangePasswordAPIView(generics.GenericAPIView):
    model = User
    permission_classes = [IsAuthenticated]
    serializer_class = ChangePasswordSerializer

    def get_object(self, queryset=None):
        obj = self.request.user
        return obj

    def put(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            if not self.object.check_password(serializer.data.get("old_password")):
                print(serializer.data.get("new_password1"))
                return Response(
                    {"old password": "wrong password"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            self.object.set_password(serializer.data.get("new_password1"))
            self.object.save()
            return Response(
                {"details": "password changed successfully"},
                status=status.HTTP_200_OK,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ActivationConfirmView(APIView):
    def get(self, request, *args, **kwargs):
        jwt_token = kwargs["jwt_token"]
        try:
            decoded_token = jwt.decode(
                jwt_token, settings.SECRET_KEY, algorithms=["HS256"]
            )
            user_id = decoded_token.get("user_id")
            print(user_id)
        except ExpiredSignatureError:
            return Response(
                {"detail": "your token is expired"},
                status=status.HTTP_408_REQUEST_TIMEOUT,
            )
        except InvalidSignatureError:
            return Response(
                {"detail": "your token is invalid"},
                status=status.HTTP_408_REQUEST_TIMEOUT,
            )
        user_obj = User.objects.get(pk=user_id)
        if user_obj.is_verified:
            return Response({"details": "your account has already been verified"})

        user_obj.is_verified = True
        user_obj.save()
        return Response(
            {"details": "your account has been verified"}, status=status.HTTP_200_OK
        )


class ProfileAPIView(generics.RetrieveUpdateAPIView):
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request):
        profile = Profile.objects.get(user=request.user)
        return Response(self.serializer_class(profile).data)
