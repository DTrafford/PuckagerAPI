import subprocess
from datetime import date, timedelta
import sys
import pymongo

sys.stdout = open("../Scouting_Twits/hist/driver_fetch_twits_output_log.txt", "a+")

list_of_keys = ['dgf', 'hockey', 'score', 'goal', 'save']
end = '2016-01-01'

def fetch_data(key, end):
    cmd = 'python3 fetch_twits_hist.py' + key + ' ' + end
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
    p.communicate()

def check_if_exits(key, end, todays_date):
    client = pymongo.MongoClient('localhost', 27017)
    mng_db = client['dgf_twits']
    db_cm = mng_db[key]
    query = {}
    db_query = db_cm.find(query)
    has_data = []
    for entry in db_query:
        has_data.append(entry)
    if not has_data:
        print('No data for collection : ' + key)
        yesterday_date = end
    else:
        yesterday_date = todays_date - timedelta(1)
    return yesterday_date


def fetch_EOD(end):
    todays_date = date.today()
    print('Todays date is :', todays_date)

    for x in list_of_keys:
        key = x
        yesterday_date = check_if_exits(x, end, todays_date)
        print('Fetching data until date :', yesterday_date)
        end = str(yesterday_date)
        print('Fetching data for key :', key)
        fetch_data(key, end)
        print('Successfully fetched data for symbol :', key)
    print('----------------------------------------------------')

if __name__ == "__main__":
    fetch_EOD(end)
