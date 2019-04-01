from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Tweet(models.Model):
    tweet_url = models.CharField(max_length=100)
    # created_by = models.ForeignKey(User, on_delete=models.CASCADE) 
    # pub_date = models.DateTimeField(auto_now=True)

    def __str__(self): 
        return self.tweet_url
