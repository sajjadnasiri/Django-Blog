from django.conf import settings
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from jwt.exceptions import ExpiredSignatureError, InvalidSignatureError
import jwt
from mail_templated import EmailMessage
from ..util import SendMail
from .serializers import SignUpSerializer
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

            detail = {"details": email + " created successfully",
                      "Click here to verify your profile": "http://127.0.0.1:8000/" + token}
            return Response(detail, status=status.HTTP_201_CREATED)
        return Response({"details": "Bad request"}, status=status.HTTP_400_BAD_REQUEST)


    def token_generator(self, user):
        refresh = RefreshToken.for_user(user)
        return str(refresh.access_token)