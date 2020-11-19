import requests
import pandas as pd
import os
import csv

start = pd.Timestamp('2014-11-28 00:00:00')
end = pd.Timestamp('2020-07-25 00:00:00')

def to_unix(ts):
    """
    Timestamp to Unix
    Args:
        ts (STR): time string

    Returns:
        Unix Timestamp.

    """
    return (pd.Timestamp(ts) - pd.Timestamp("1970-01-01")) // pd.Timedelta('1s')

subreddits = ['Bitcoin', 'CryptoCurrency']

start_epoc = to_unix(start)
end_epoc = to_unix(end)

# Comment & Submission Volume
def get_reddit_vol(start_epoc, end_epoc, subreddits, sub = True, freq = 'day'):
    dfs_reddit_vol = []
    if sub == True:
        url = 'https://api.pushshift.io/reddit/search/submission/'
        filename = "data//reddit//reddit_submissions_vol.csv"
    else:
        url = 'https://api.pushshift.io/reddit/search/comment/'
        filename = "data//reddit//reddit_comments_vol.csv"
    
    for subreddit in subreddits:
        parameters = {
            'subreddit' : subreddit,
            'size' : 0,
            'after' : start_epoc,
            'before' : end_epoc,
            'aggs' : 'created_utc',
            'frequency' : freq,
            }
        response = requests.get(url = url, params = parameters)
        df_reddit_vol = pd.DataFrame(response.json()['aggs']['created_utc'])
        dfs_reddit_vol.append(df_reddit_vol)
    
    reddit_vol = pd.DataFrame(columns = ['count','date'])
    reddit_vol['count'] = dfs_reddit_vol[0]['doc_count'] + dfs_reddit_vol[1]['doc_count']
    reddit_vol['date'] = df_reddit_vol['key']
    reddit_vol['date'] = pd.to_datetime(reddit_vol['date'], unit = 's')
    reddit_vol = reddit_vol.set_index('date')
    reddit_vol.to_csv(filename)
    return reddit_vol


# Total submissions & comments volume:
def get_reddit_totalvol(start_epoc, end_epoc, subreddits):
    reddit_volsub = get_reddit_vol(start_epoc, end_epoc, subreddits)
    reddit_volcmt = get_reddit_vol(start_epoc, end_epoc, subreddits, sub = False)
    reddit_vol = pd.merge(reddit_volsub, reddit_volcmt, 
                            left_index = True, right_index = True,
                            suffixes=['_sub','_cmt'])
    reddit_vol['count'] = reddit_vol['count_cmt'] + reddit_vol['count_sub']
    reddit_vol.to_csv("data//reddit//reddit_total_vol.csv")
    return reddit_vol

# Detailed submissions and comments

def get_reddit_subs(subreddit,start_epoc, end_epoc, filename):
    base_url = 'https://api.pushshift.io/reddit/search/submission/?'
    fields = ['id', 'created_utc', 'title', 'content', 'author']
    
    fixed_params = (
        f'size=500&'
        f'before={end_epoc}&'
        f'fields=author,id,created_utc,title,selftext,subreddit&'
        ) 
    
    file = open(filename, 'a', newline='', encoding ='utf-8')
    if os.stat(filename).st_size == 0:
        # OPEN FILE IN APPEND MODE AND WRITE HEADERS TO FILE
        last_submission_time = None
        csvfile = csv.DictWriter(file, fields)
        csvfile.writeheader()
    else:
        # FIRST EXTRACT LAST submission ID THEN OPEN FILE IN APPEND MODE WITHOUT WRITING HEADERS
        file = open(filename, 'r', newline='', encoding='utf-8')
        csvfile = csv.DictReader((line.replace('\0', '') for line in file))
        data = list(csvfile)
        data = data[-1]
        last_submission_time = data['created_utc']
        file.close()
        file = open(filename, 'a', newline='', encoding='utf-8')
        csvfile = csv.DictWriter(file, fields)
    
    if last_submission_time is not None and start_epoc < int(last_submission_time):
        start_epoc = last_submission_time
    api_calls = 0
    while True:
        try:
            full_params = (f'{fixed_params}'
                           f'subreddit={subreddit}&'
                           f'after={start_epoc}'
                           )
            response = requests.get(url = base_url+full_params)
        except Exception:
            response = None
            
        if response is not None:
            if response.status_code == 429:
                print("REACHED RATE LIMITED 120/min.")
            if response.status_code != 200:
                continue
            
        dict_reddit_sub = response.json()['data']
        if dict_reddit_sub != []:
            start_epoc = dict_reddit_sub[-1]['created_utc']
            api_calls += 1
            print(f"API CALL NO: {api_calls} {subreddit}")  
        else:
            print("FINISHED!")
            break
        
        for submission in dict_reddit_sub:
            obj = {}
            obj['author'] = submission['author']
            obj['id'] = submission['id']
            obj['created_utc'] = submission['created_utc']
            obj['title'] = submission['title']
            if 'selftext' in submission.keys():
                obj['content'] = submission['selftext']
            else:
                obj['content'] = ""
            csvfile.writerow(obj)
            file.flush()
    file.close()
   
def get_reddit_cmts(subreddit,start_epoc, end_epoc, filename):
    base_url = 'https://api.pushshift.io/reddit/search/comment/?'
    fields = ['id', 'created_utc', 'content', 'author']
    
    fixed_params = (
        f'size=500&'
        f'before={end_epoc}&'
        f'fields=author,id,created_utc,body,subreddit&'
        ) 
    
    file = open(filename, 'a', newline='', encoding ='utf-8')
    if os.stat(filename).st_size == 0:
        # OPEN FILE IN APPEND MODE AND WRITE HEADERS TO FILE
        last_comment_time = None
        csvfile = csv.DictWriter(file, fields)
        csvfile.writeheader()
    else:
        # FIRST EXTRACT LAST submission ID THEN OPEN FILE IN APPEND MODE WITHOUT WRITING HEADERS
        file = open(filename, 'r', newline='', encoding='utf-8')
        csvfile = csv.DictReader((line.replace('\0', '') for line in file))
        data = list(csvfile)
        data = data[-1]
        last_comment_time = data['created_utc']
        file.close()
        file = open(filename, 'a', newline='', encoding='utf-8')
        csvfile = csv.DictWriter(file, fields)
    
    if last_comment_time is not None and start_epoc < int(last_comment_time):
        start_epoc = last_comment_time
    api_calls = 0
    while True:
        try:
            full_params = (f'{fixed_params}'
                           f'subreddit={subreddit}&'
                           f'after={start_epoc}'
                           )
            response = requests.get(url = base_url+full_params)
        except Exception:
            response = None
            
        if response is not None:
            if response.status_code == 429:
                print("REACHED RATE LIMITED 120/min.")
            if response.status_code != 200:
                continue
            
            dict_reddit_sub = response.json()['data']
            if dict_reddit_sub != []:
                start_epoc = dict_reddit_sub[-1]['created_utc']
                api_calls += 1
                print(f"API CALL NO: {api_calls} {subreddit}")  
            else:
                print("FINISHED!")
                break
            
            for comment in dict_reddit_sub:
                obj = {}
                obj['author'] = comment['author']
                obj['id'] = comment['id']
                obj['created_utc'] = comment['created_utc']
                obj['content'] = comment['body']
                csvfile.writerow(obj)
                file.flush()
    file.close()
    
if __name__ == '__main__':
    subreddit = subreddits[1]
    get_reddit_cmts(subreddit,start_epoc, end_epoc, filename = f"data//reddit//comments_{subreddit}.csv")
