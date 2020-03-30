import operator
import sys
import json
from collections import Counter
import re
from nltk.corpus import stopwords
import string
from collections import defaultdict
from Scouting_Twits import process_tweet

punctuation = list(string.punctuation)
stop = stopwords.words('english') + punctuation + ['rt', 'via']

fname = 'twitter_data.json'
with open(fname, 'r') as f:
    com = defaultdict(lambda: defaultdict(int))
    search_word = sys.argv[1]  # pass a term as a command-line argument
    count_search = Counter()

# f is the file pointer to the JSON data set
    for line in f:
        tweet = json.loads(line)
        terms_only = [term for term in process_tweet.preprocess(tweet['text'])
                      if term not in stop
                      and not term.startswith(('#', '@'))]
        if search_word in terms_only:
            count_search.update(terms_only)
        # Build co-occurrence matrix
        for i in range(len(terms_only) - 1):
            for j in range(i + 1, len(terms_only)):
                w1, w2 = sorted([terms_only[i], terms_only[j]])
                if w1 != w2:
                    com[w1][w2] += 1
        com_max = []
        # For each term, look for the most common co-occurrent terms
        for t1 in com:
            t1_max_terms = sorted(
                com[t1].items(), key=operator.itemgetter(1), reverse=True)[:5]
            for t2, t2_count in t1_max_terms:
                com_max.append(((t1, t2), t2_count))
        # Get the most frequent co-occurrences
        terms_max = sorted(com_max, key=operator.itemgetter(1), reverse=True)
        print(terms_max[:5])

    print("Co-occurrence for %s:" % search_word)
    print(count_search.most_common(20))

    from nltk import bigrams

    terms_bigram = bigrams(terms_only)
    for t in terms_bigram:
        print(t)
