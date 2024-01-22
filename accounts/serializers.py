from .models import User
from rest_framework import serializers
from django.utils.http import urlsafe_base64_decode,urlsafe_base64_encode
from rest_framework import serializers
from .models import User
from django.contrib.auth import authenticate, login
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import smart_str,force_str,DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode,urlsafe_base64_encode
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse




class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, style={'input_type': 'password'})

    class Meta:
        model = User
        fields = ['id', 'name', 'email', 'phone', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(
            email=validated_data['email'],
            phone=validated_data['phone'],
            password=validated_data['password'],
            name=validated_data['name']
        )
        return user




class ResetPasswordEmailRequestSerializer(serializers.Serializer):
    email =serializers.EmailField(min_length=2)

    class Meta:
        model=User
        fields =['email']


class SetNewPasswordSerializer(serializers.Serializer):
    password=serializers.CharField(min_length=1,max_length=68,write_only=True)
    token=serializers.CharField(min_length=1,write_only=True)
    uidb64=serializers.CharField(min_length=1,write_only=True)


    class Meta:
        fields=['password','token','uidb64']


    def validate(self, attrs):
        try:
            password=attrs.get('password')
            token=attrs.get('token')
            uidb64=attrs.get('uidb64')

            id =force_str(urlsafe_base64_decode(uidb64))
            user=(User.objects.get(id=id))

            if not PasswordResetTokenGenerator().check_token(user,token):
                return('no valid link')
            user.set_password(password)
            user.save()
        except Exception as e:
            return('ok valid link')

        return super().validate(attrs)