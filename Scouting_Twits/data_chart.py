import re
import json
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from Scouting_Twits import twitter_streaming

tweets_data_path = 'data/twitter_data.json'

tweets_data = []
tweets_file = open(tweets_data_path, "r")
for line in tweets_file:
    try:
        tweet = json.loads(line)
        tweets_data.append(tweet)
    except:
        continue
print(len(tweets_data))
tweets = pd.DataFrame()
