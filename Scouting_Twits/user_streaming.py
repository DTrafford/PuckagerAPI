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

# data = open(os.path.join(BASE, "snp_data.txt"))

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

# tweets_data_path = 'data/player_raw_data'+player_name+'.json'
tweets_data_path = os.path.join(BASE, 'data/twitter_data.json')

tweets_data = []
# tweets_file = open(tweets_data_path, "r")
tweets_file = open(tweets_data_path)

# # tweets_data_path = 'data/player_raw_data_'+player_name+'.json'
# tweets_data_path = os.path.join(BASE, 'data/twitter_data.json')
#
# tweets_data = []
# tweets_file = open(tweets_data_path)


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
            new_tweets = api.search(q=name, count=count, max_id=str(last_id - 1))
            print('NEW TWEETS = ', new_tweets)
            if not new_tweets:
                break
            for tweet in new_tweets['statuses']:
                serached_tweets.append(tweet)
            # serached_tweets.extend(new_tweets)
            # print(serached_tweets)
            # print(new_tweets['statuses'][0]['id'])
            last_id = new_tweets['statuses'][0]['id']
        except tweepy.TweepError as e:
            break
    return serached_tweets

    # for status in tweepy.Cursor(api.search, q=name).items(10):
    #     stream = Stream(auth, TwitterListener(status))
    #     list_of_keywords.keywords.append(name)
    #     # stream.filter(track=list_of_keywords.keywords)
    #     stream.filter(track=keywords_to_search)
    #     stream.filter(follow=user.id)
    #     stream.filter(location='Canada')
    #     stream.filter(count=10)
    #     stream.filter(limit=10)
    #     stream.filter(async=True)




    ####### GABRIELE CODE ############
    # player_name = name
    # user = api.get_user(screen_name=name)
    # stream = Stream(auth, TwitterListener())

    # # stream.filter(follow=user,track=list_of_keywords.keywords)
    # # stream.filter(track=list_of_keywords.keywords)
    # keywords_to_search = list_of_keywords.keywords
    # keywords_to_search.append(name)
    # print('NAME IN USER_STREAM', name)
    # # stream.filter(track=keywords_to_search)
    # stream.filter(track=keywords_to_search)
    # stream.filter(follow=user.id)
    # stream.filter(location='Canada')
    # stream.filter(count=10)
    # stream.filter(limit=10)
    # stream.filter(async=True)

###################################
    # Tyler's cursor limitation code
    # # user = list(tweepy.Cursor(api.search, q=name, result_type='recent').items(10))
    # for status in tweepy.Cursor(api.search, q=name).items(10):
    #     stream = Stream(auth, TwitterListener(status))
    #     list_of_keywords.keywords.append(name)
    #     # stream.filter(track=list_of_keywords.keywords)
    #     stream.filter(track=keywords_to_search)
    #     stream.filter(follow=user.id)
    #     stream.filter(location='Canada')
    #     stream.filter(count=10)
    #     stream.filter(limit=10)
    #     stream.filter(async=True)


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

    # print(data)
    for i in range(0,len(data)):
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
        # finally include the line into the dict
        # print(output_data)
        # TODO WHYYYYYY DOES THIS COPY LAST LINE TO EVERY LINE
        output_json.append(output_data)
    # output_json = json.dumps(output_data)

    return output_json



    # df = pd.DataFrame()
    # df['']

if __name__ == '__main__':
    user_stream("Gretzky")
    output = scrape_raw_data_by_user(tweets_file)
    # print(output)
    pprint.pprint(output)
