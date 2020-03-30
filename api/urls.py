from django.urls import include, re_path, path
from .apiviews import TweetList
from .apiviews import TweetViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('api', TweetViewSet, base_name='api')


urlpatterns = [
    path("twitter/", TweetList.as_view(), name="tweet_list"),
]

urlpatterns += router.urls
