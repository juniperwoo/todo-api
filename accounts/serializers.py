import re
from rest_framework import serializers
from .models import User


class RegisterSerializer(serializers.ModelSerializer): #serializer for user registration, includes password validation
    password  = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)

    class Meta:
        model  = User
        fields = ('id', 'username', 'email', 'password', 'password2')

    def validate_password(self, value):
        if len(value) < 8:
            raise serializers.ValidationError("Password must be at least 8 characters long.")
        if not re.search(r'[A-Z]', value):
            raise serializers.ValidationError("Password must contain at least one uppercase letter.")
        if not re.search(r'[a-z]', value):
            raise serializers.ValidationError("Password must contain at least one lowercase letter.")
        if not re.search(r'[0-9]', value):
            raise serializers.ValidationError("Password must contain at least one number.")
        if not re.search(r'[!@#$%^&*(),.?\":{}|<>]', value):
            raise serializers.ValidationError("Password must contain at least one special character.")
        return value
    
    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("A user with this email already exists.")
        return value

    def validate(self, data):
        if data['password'] != data['password2']:
            raise serializers.ValidationError({"password": "Passwords do not match."})
        return data

    def create(self, validated_data):  
        validated_data.pop('password2')
        user = User.objects.create_user(
            username=validated_data['username'], 
            email=validated_data.get('email', ''), 
            password=validated_data['password']  
        )
        return user


class UserSerializer(serializers.ModelSerializer): #serializer for user model to show user details in api response  
    class Meta: #meta class to specify the model and fields to be serialized
        model  = User 
        fields = ('id', 'username', 'email', 'created_at', 'updated_at')
        read_only_fields = ('id', 'created_at', 'updated_at')