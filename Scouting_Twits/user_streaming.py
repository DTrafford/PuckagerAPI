# TODO WORKING STREAM CODE USE THIS TYLER

import tweepy
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import json
import matplotlib
import pandas as pd
import numpy as np
from Scouting_Twits.config import list_of_keywords
import pprint
import os.path
BASE = os.path.dirname(os.path.abspath(__file__))

# Variables that contains the user credentials to access Twitter API
# region  NOT FOR PUBLIC EYES
access_token = "1105994278289838081-KnlpnzyLPWh008p7UlubKDNNI9E4oN"
access_token_secret = "5NopQKoZycsOoOATfYDzdf8Ujx3oGLSC8Lwyj7ks1HILz"
consumer_key = "9Z49YWOPFiwAolKQbZFxdvXFy"
consumer_secret = "b1PIijzElDvAcUzayEYwJ2tNx34QqFJcqwqWGK8ptExPGiupnM"
# endregion

auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth, parser=tweepy.parsers.JSONParser())

player_name = ''

tweets_data_path = os.path.join(BASE, 'data/twitter_data.json')

tweets_data = []

tweets_file = open(tweets_data_path)


class TwitterListener(StreamListener):

    def on_data(self, data):
        # print(data)
        # return True
        try:
            print("Listening for data...")
            with open(tweets_data_path, 'a') as f:
                f.write(data)
                print("Writing data...")
                return data
        except BaseException as e:
            print("Error on_data: %s" % str(e))
        return True

    def on_error(self, status):
        print(status)
        return True


def user_stream(name):
    serached_tweets = []
    max_tweets = 10
    last_id = -1
    while len(serached_tweets) < max_tweets:
        count = max_tweets - len(serached_tweets)
        try:
            new_tweets = api.search(
                q=name, count=count, max_id=str(last_id - 1))
            print('NEW TWEETS = ', new_tweets)
            if not new_tweets:
                break
            for tweet in new_tweets['statuses']:
                serached_tweets.append(tweet)

            last_id = new_tweets['statuses'][0]['id']
        except tweepy.TweepError as e:
            break
    return serached_tweets


def scrape_raw_data_by_user(data_path):
    data = []
    for line in data_path:
        try:
            tweet = json.loads(line)
            # print(tweet)
            data.append(tweet)
        except:
            continue
    output_json = []
    output_data = {}

    for i in range(0, len(data)):
        # print(str(i))
        output_data["row"] = str(i)
        output_data['id'] = data[i]['id']
        output_data['text'] = data[i]["text"].strip()
        output_data['created_at'] = data[i]["created_at"]
        output_data['source'] = data[i]['source']
        output_data['user_name'] = data[i]["user"]["name"]
        output_data['user_id'] = data[i]["user"]["id"]
        output_data['user_location'] = data[i]["user"]["location"]
        # TODO something wrong with 'url'
        try:
            output_data['url'] = data["url"]
        except:
            pass

        output_json.append(output_data)

    return output_json


if __name__ == '__main__':
    user_stream("Gretzky")
    output = scrape_raw_data_by_user(tweets_file)
    pprint.pprint(output)
