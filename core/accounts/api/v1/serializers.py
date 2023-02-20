from django.core import exceptions
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth import authenticate
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from ...models import User, Profile


class SignUpSerializer(serializers.ModelSerializer):
    pass_confirm = serializers.CharField(
        max_length=255, write_only=True,
        style={'input_type': 'password'}
    )

    class Meta:
        model = User
        fields = ('email', 'password', 'pass_confirm')

    def validate(self, attrs):
        if attrs.get('password') != attrs.get('pass_confirm'):
            raise serializers.ValidationError({"details": "passwords does not match"})
        
        try:
            validate_password(attrs.get('password'))
        except exceptions.ValidationError as E:
            raise serializers.ValidationError({"Password": list(E.messages)})

        return super().validate(attrs)

    def create(self, validated_data):
        validated_data.pop("pass_confirm")
        return User.objects.create_user(**validated_data)
    

class CustomObtainTokenSerializer(serializers.Serializer):
    email = serializers.CharField(label=("email"), write_only=True)
    password = serializers.CharField(
        label=("Password"),
        style={"input_type": "password"},
        trim_whitespace=False,
        write_only=True,
    )
    token = serializers.CharField(label=_("Token"), read_only=True)
    def validate(self, attrs):
        username = attrs.get("email")
        password = attrs.get("password")

        if username and password:
            user = authenticate(
                request=self.context.get("request"),
                username=username,
                password=password,
            )
            if not user:
                msg = _("unable to log in with provided credentials")
                raise serializers.ValidationError({"details": msg})
            if not user.is_verified:
                raise serializers.ValidationError({"details": "This user is not verified"})
        else:
            msg = _("must include email and password")
            raise serializers.ValidationError({"details": msg})
        
        attrs["user"] = user
        return attrs


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        validated_data = super().validate(attrs)
        if not self.user.is_verified:
            raise serializers.ValidationError({"details": "user is not verified"})
        validated_data["email"] = self.user.email
        validated_data["user_id"] = self.user.id
        validated_data["first_name"] = Profile.objects.get(user=self.user).first_name
        validated_data["last_name"] = Profile.objects.get(user=self.user).last_name
        return validated_data
    

class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True, max_length=255, style={'input_type': 'password'})
    new_password1 = serializers.CharField(required=True, max_length=255, style={'input_type': 'password'})
    new_password2 = serializers.CharField(required=True, max_length=255, style={'input_type': 'password'})

    def validate(self, attrs):
        if attrs.get('new_password1') != attrs.get('new_password2'):
            raise serializers.ValidationError({"details":
                                               "password dosnt match"})
        try:
            validate_password(attrs.get("new_password1"))
        except exceptions.ValidationError as e:
            raise serializers.ValidationError({"new_password1": list(e.messages)})

        return super().validate(attrs)


class ProfileSerializer(serializers.ModelSerializer):
    email = serializers.CharField(source="user.email", read_only=True)
    class Meta:
        model = Profile
        fields = "__all__"
        read_only_fiels = "email"
