from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from .models import Tweet

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User(
            email=validated_data['email'],
            username=validated_data['username']
        )
        user.set_password(validated_data['password'])
        user.save()
        token = Token.objects.create(user=user)
        print('TOKEN = ', token)
        return user

class TweetSerializer(serializers.ModelSerializer):
    
    class Meta: 
        model = Tweet
        fields = '__all__'
    