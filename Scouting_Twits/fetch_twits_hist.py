import json, sys
import requests
import pandas as pd
import time
import datetime as dt
import pymongo
pd.set_option('display.width',1000)
from datetime import datetime

sys.stdout = open("../Scouting_Twits/hist/driver_fetch_twits_output_log.txt", "a+")
starttime = dt.datetime.now()


# TODO create a slack_msg def to send updates

def write_to_db(df,key,last_record):
    try:
        client = pymongo.MongoClient('localhost', 27017)
        mng_db = client['dgf_twits']
        db_cm = mng_db[key]
        df.reset_index(inplace=True)
        df.drop('index', axis=1, inplace=True)
        df.set_index('id')
        print('Time stamp : ', dt.datetime.now(), '--->  Successfully set index: id in dataframe')
        df_json = json.loads(df.T.to_json()).values()
        print('Time stamp : ', dt.datetime.now(), '--->  Successfully converted data to Json format')

        for x in df_json:
            id = x['id']
            db_cm.update({'id': id}, x, upsert=True)

        print('Time stamp : ', dt.datetime.now(), '--->  Successfully Updated Mongo DB, collection : ', key)

    except Exception as ex:
        print('Time stamp : ', dt.datetime.now(),
              '---> ', ex)
        print('Time stamp : ', dt.datetime.now(), '--->  Unable to save data to Mongo DB')
        df.to_pickle('../DGF_Twits/hist/{}_{}_{}.p'.format(key, last_record['created_at'][0:19].replace(':', '-'),
                                                 last_record['id']))
        print('Time stamp : ', dt.datetime.now(), '--->  Data saved locally to "hist" folder')
        time_stamp = dt.datetime.now()
        msg = 'Time stamp : ' + str(
            time_stamp) + ' Error occurred while writing to Mongo DB for key ' + key + ', Data saved locally to "hist" folder'
        # slack_msg(msg)

def print_response_limits(resp):
    print('RateLimit-Limit : ', resp.headers.get('X-RateLimit-Limit', ''))
    print('RateLimit-Remaining : ', resp.headers.get('X-RateLimit-Remaining', ''))
    print('RateLimit-Reset : ', dt.datetime.fromtimestamp(int(resp.headers.get('X-RateLimit-Reset', 0))))
    print("---------------------------------------------------------------------------------------------------------------")

def last_tweet_date(key, last_record, max_date):
    try:
        # max_date = '2016-01-01'
        max_date = datetime.strptime(max_date, "%Y-%m-%d").date()
        tweet_date = last_record['created_at']
        tweet_date = tweet_date[0:10]
        tweet_date = datetime.strptime(tweet_date, "%Y-%m-%d").date()
        print('Tweet date:', tweet_date)
        print('Max tweet date:', max_date)
        if tweet_date < max_date:
            print('Time stamp : ', dt.datetime.now(),
                  "--->  Successfully fetched all data for " + key + ", exiting script...")
            time_stamp = dt.datetime.now()
            msg = 'Time stamp : ' + str(
                time_stamp) + ' Successfully fetched all data for ' + key + ', exiting script...'
            # slack_msg(msg)
            sys.exit()
    except Exception as ex:
        print('Time stamp : ', dt.datetime.now(),
              '--->  ', ex)
        print('Time stamp : ', dt.datetime.now(),
              '--->  Error occurred while parsing the date of last fetched tweet...' + str(ex))
        time_stamp = dt.datetime.now()
        msg = 'Time stamp : ' + str(
            time_stamp) + ' Error occurred while parsing the date of last fetched tweet... ' + str(ex)
        # slack_msg(msg)


