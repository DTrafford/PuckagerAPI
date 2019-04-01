from rest_framework import generics, viewsets
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.contrib.auth import authenticate

from Scouting_Twits import user_streaming

from .models import Tweet
from .serializers import TweetSerializer, UserSerializer

# class UserCreate(generics.CreateAPIView):
#     authentication_classes = ()
#     permission_classes = ()
#     serializer_class = UserSerializer

# class LoginView(APIView):
#     permission_classes = ()

#     def post(self, request):
#         username = request.data.get('username')
#         password = request.data.get('password')
#         user = authenticate(username=username, password=password)
#         if user:
#             return Response({"token": user.auth_token.key})
#         else:
#             return Response({'error': 'Wrong Credentials'}, status=status.HTTP_400_BAD_REQUEST)
## USING VIEWSET ##
class TweetViewSet(viewsets.ModelViewSet):
    # queryset = Tweet.objects.all()
    queryset = 'TWEET_VIEW_SET'
    serializer_class = TweetSerializer
    # serializer_class = TweetSerializer
    print('IN TWEETVIEWSET')

## USING GENERIC VIEWW ###
# class TweetList(generics.ListAPIView):
class TweetList(APIView):
    def post(self, request):
        print("REQUEST = ", request.data)
        # print("REQUEST = ", request.options)
        twitter_data = user_streaming.user_stream(request.data['player_name'])
        print("TWITTER DATA = ", twitter_data)
        return Response(twitter_data)
    # queryset = Tweet.objects.all()

    # # THIS WILL PRINT THE OBJECTS IN THE DEBUGGER
    # test = [i for i in Tweet.objects.all()]

    # print(queryset)

    # serializer_class = TweetSerializer


# class PollDetail(generics.RetrieveDestroyAPIView):
#     queryset = Poll.objects.all()
#     serializer_class = PollSerializer


# class ChoiceList(generics.ListCreateAPIView):
#     def get_queryset(self):
#         queryset = Choice.objects.filter(poll_id=self.kwargs["pk"])
#         return queryset
#     serializer_class = ChoiceSerializer


# class CreateVote(generics.CreateAPIView):
#     def post(self, request, pk, choice_pk):
#         voted_by = request.data.get("voted_by")
#         data = {'choice': choice_pk, 'poll': pk, 'voted_by': voted_by} 
#         serializer = VoteSerializer(data=data)
#         if serializer.is_valid():
#             vote = serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED) 
#         else:
#             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

## This is the pure django way ##

# class PollList(APIView):
#     def get(self, request):
#         polls = Poll.objects.all()[:20]
#         data = PollSerializer(polls, many=True).data
#         return Response(data)

#     # def post(self, request, data):
#     #     polls = Poll.objects.all()
#     #     polls.append(data);

# class PollDetail(APIView):
#     def get(self, reuqest, pk):
#         poll = get_object_or_404(Poll, pk=pk)
#         data = PollSerializer(poll).data
#         return Response(data)
