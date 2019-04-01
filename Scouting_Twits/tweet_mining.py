import re
import json
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import django
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

def word_in_text(word, text):
    word = word.lower()
    text = text.lower()
    match = re.search(word, text)
    if match:
        return True
    return False

# check if word in tweet df
tweets['hockey'] = tweets['text'].apply(lambda tweet: word_in_text('hockey', tweet))
tweets['dgf'] = tweets['text'].apply(lambda tweet: word_in_text('dgf', tweet))
tweets['puckager'] = tweets['text'].apply(lambda tweet: word_in_text('puckager', tweet))

# count number of tweets with keyword mentions
print(tweets['hockey'].value_counts()[True])
print(tweets['dgf'].value_counts()[True])
print(tweets['puckager'].value_counts()[True])

# create simple chaet based on the mining results
# TODO refactor all manual keyword entries into an array of kekywords and loop through it when mining
prg_langs = ['hockey', 'dgf', 'puckager']
tweets_by_prg_lang = [tweets['hockey'].value_counts()[True], tweets['dgf'].value_counts()[True], tweets['puckager'].value_counts()[True]]

x_pos = list(range(len(prg_langs)))
width = 0.8
fig, ax = plt.subplots()
plt.bar(x_pos, tweets_by_prg_lang, width, alpha=1, color='g')

# Setting axis labels and ticks
ax.set_ylabel('Number of tweets', fontsize=15)
ax.set_title('Ranking: vs(Raw data)', fontsize=10, fontweight='bold')
ax.set_xticks([p + 0.4 * width for p in x_pos])
ax.set_xticklabels(prg_langs)
plt.grid()


# target tweets
