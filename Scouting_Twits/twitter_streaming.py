# TODO SIMILAR TO USER STREAMING BUT PULLS ALL CODE

import tweepy
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import json
import matplotlib
import pandas as pd
import numpy as np

# Variables that contains the user credentials to access Twitter API
# region  NOT FOR PUBLIC EYES
access_token = "1105994278289838081-KnlpnzyLPWh008p7UlubKDNNI9E4oN"
access_token_secret = "5NopQKoZycsOoOATfYDzdf8Ujx3oGLSC8Lwyj7ks1HILz"
consumer_key = "9Z49YWOPFiwAolKQbZFxdvXFy"
consumer_secret = "b1PIijzElDvAcUzayEYwJ2tNx34QqFJcqwqWGK8ptExPGiupnM"
# endregion


# This is a basic listener that just prints received tweets to stdout.
class TwitterListener(StreamListener):

    def on_data(self, data):
        # print(data)
        # return True
        try:
            print("Listening for data...")
            with open('data/twitter_data.json', 'a') as f:
                f.write(data)
                print("Writing data...")
                return True
        except BaseException as e:
            print("Error on_data: %s" % str(e))
        return True

    def on_error(self, status):
        print(status)
        return True


if __name__ == '__main__':

    # This handles Twitter authentication and the connection to Twitter Streaming API
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth)

    stream = Stream(auth, TwitterListener())
    # This line filter Twitter Streams to capture data by the keywords
    # stream.filter(track=['dgf', 'hockey', 'score', 'goal', 'save'])
