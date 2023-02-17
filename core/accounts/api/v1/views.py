from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework import status
from .serializers import SignUpSerializer
import jwt
from jwt.exceptions import ExpiredSignatureError, InvalidSignatureError
from ...models import User, Profile
from django.conf import settings


class SignUpAPIView(generics.GenericAPIView):
    serializer_class = SignUpSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            serializer.save()
            detail = {"details": serializer.validated_data["email"] + " created successfully"}
            return Response(detail, status=status.HTTP_201_CREATED)
        return Response({"details": "Bad request"}, status=status.HTTP_400_BAD_REQUEST)


