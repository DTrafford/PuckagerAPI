from rest_framework import generics, viewsets
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.contrib.auth import authenticate

from Scouting_Twits import user_streaming

from .models import Tweet
from .serializers import TweetSerializer, UserSerializer

## USING VIEWSET ##


class TweetViewSet(viewsets.ModelViewSet):
    queryset = 'TWEET_VIEW_SET'
    serializer_class = TweetSerializer
    print('IN TWEETVIEWSET')

## USING GENERIC VIEWW ###


class TweetList(APIView):

    def get(self, requste):
        return Response('IN GET')

    def post(self, request):
        print("REQUEST = ", request.data)
        twitter_data = user_streaming.user_stream(request.data['player_name'])
        print("TWITTER DATA = ", twitter_data)
        return Response(twitter_data)
