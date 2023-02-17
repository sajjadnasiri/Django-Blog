from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from django.core import exceptions
from ...models import User, Profile


class SignUpSerializer(serializers.ModelSerializer):
    pass_confirm = serializers.CharField(max_length=255, write_only=True)

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
    