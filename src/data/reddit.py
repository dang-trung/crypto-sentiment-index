#!/usr/bin/env python3
"""Get Reddit Comments & Submissions

This module defines functions that download Reddit comments and submissions
using Pushshift.io API.
"""
import csv
import os

import pandas as pd
import requests
from requests.exceptions import HTTPError

from .convert_ts import ts_to_unix


def get_submissions(subreddit, start_unix, end_unix, file_name):
    """
    Get Reddit Comments in detail and export to a .csv file.

    Parameters
    ----------
    subreddit : str
        Name of Subreddit.
    start_unix : int
        Epoch (Unix) Time in Seconds.
    end_unix : int
        Epoch (Unix) Time in Seconds.
    file_name : str
        File path.

    Returns
    -------
    NoneType
        None.
    """
    print(f"Getting submissions from the subreddit {subreddit}")
    base_url = 'https://api.pushshift.io/reddit/search/submission/?'
    fields = ['id', 'created_utc', 'title', 'content', 'author']

    fixed_params = (
        f'size=500&'
        f'before={end_unix}&'
        f'fields=author,id,created_utc,title,selftext,subreddit&'
    )

    file = open(file_name, 'a', newline='', encoding='utf-8')
    if os.stat(file_name).st_size == 0:
        # Open file in append mode and write headers to file
        last_submission_time = None
        csvfile = csv.DictWriter(file, fields)
        csvfile.writeheader()
    else:
        # Check the last submission id then open file in append mode without
        # writing headers
        file = open(file_name, 'r', newline='', encoding='utf-8')
        csvfile = csv.DictReader((line.replace('\0', '') for line in file))
        data = list(csvfile)
        data = data[-1]
        last_submission_time = data['created_utc']
        file.close()
        file = open(file_name, 'a', newline='', encoding='utf-8')
        csvfile = csv.DictWriter(file, fields)

    if last_submission_time is not None and start_unix < int(
            last_submission_time):
        start_unix = last_submission_time
    api_calls = 0
    while True:
        try:
            full_params = (f'{fixed_params}'
                           f'subreddit={subreddit}&'
                           f'after={start_unix}'
                           )
            response = requests.get(url=base_url + full_params)
        except HTTPError as http_err:
            print(f'HTTP error occurred: {http_err}')
            response = None
        except Exception as err:
            print(f'Other error occurred: {err}')
            response = None

        if response is not None:
            if response.status_code == 429:
                print("REACHED RATE LIMITED 120/min.")
            if response.status_code != 200:
                continue

        dict_reddit_sub = response.json()['data']
        if dict_reddit_sub:
            start_unix = dict_reddit_sub[-1]['created_utc']
            api_calls += 1
            print(f"API CALLs: {api_calls} {subreddit}")
        else:
            print("FINISHED!")
            break

        for submission in dict_reddit_sub:
            obj = {'author': submission['author'], 'id': submission['id'],
                   'created_utc': submission['created_utc'],
                   'title': submission['title']}
            if 'selftext' in submission.keys():
                obj['content'] = submission['selftext']
            else:
                obj['content'] = ""
            csvfile.writerow(obj)
            file.flush()
    file.close()
    print(f"Done {subreddit}!")
    print("-----------------")


def get_comments(subreddit, start_unix, end_unix, file_name):
    """
    Get Reddit Comments in detail and export to a .csv file.

    Parameters
    ----------
    subreddit : str
        Name of Subreddit.
    start_unix : int
        Epoch (Unix) Time in Seconds.
    end_unix : int
        Epoch (Unix) Time in Seconds.
    file_name : str
        File path.

    Returns
    -------
    NoneType
        None.

    """
    print(f"Getting comments from the subreddit {subreddit}")
    base_url = 'https://api.pushshift.io/reddit/search/comment/?'
    fields = ['id', 'created_utc', 'content', 'author']

    fixed_params = (
        f'size=500&'
        f'before={end_unix}&'
        f'fields=author,id,created_utc,body,subreddit&'
    )

    file = open(file_name, 'a', newline='', encoding='utf-8')
    if os.stat(file_name).st_size == 0:
        # Open file in append mode and write headers to file
        last_comment_time = None
        csvfile = csv.DictWriter(file, fields)
        csvfile.writeheader()
    else:
        # First extract last submission id then open file in append mode
        # without writing headers
        file = open(file_name, 'r', newline='', encoding='utf-8')
        csvfile = csv.DictReader((line.replace('\0', '') for line in file))
        data = list(csvfile)
        data = data[-1]
        last_comment_time = data['created_utc']
        file.close()
        file = open(file_name, 'a', newline='', encoding='utf-8')
        csvfile = csv.DictWriter(file, fields)

    if last_comment_time is not None and start_unix < int(last_comment_time):
        start_unix = last_comment_time
    api_calls = 0
    while True:
        try:
            full_params = (f'{fixed_params}'
                           f'subreddit={subreddit}&'
                           f'after={start_unix}'
                           )
            response = requests.get(url=base_url + full_params)
        except HTTPError as http_err:
            print(f'HTTP error occurred: {http_err}')
            response = None
        except Exception as err:
            print(f'Other error occurred: {err}')
            response = None

        if response is not None:
            if response.status_code == 429:
                print("REACHED RATE LIMITED 120/min.")
            if response.status_code != 200:
                continue

            dict_reddit_sub = response.json()['data']
            if dict_reddit_sub:
                start_unix = dict_reddit_sub[-1]['created_utc']
                api_calls += 1
                print(f"API CALLS: {api_calls} {subreddit}")
            else:
                print("FINISHED!")
                break

            for comment in dict_reddit_sub:
                obj = {'author': comment['author'], 'id': comment['id'],
                       'created_utc': comment['created_utc'],
                       'content': comment['body']}
                csvfile.writerow(obj)
                file.flush()
    file.close()
    print(f"Done {subreddit}!")
    print("-----------------")


# Temporarily Disabled by Pushshift
def get_volume(subreddits, start_unix, end_unix, freq, filename=None,
               sub=True):
    """
    Get Reddit Submissions OR Comments Volume.

    Parameters
    ----------
    subreddits : list
        List of Targeted Subreddits.
    start_unix : int
        Epoch (Unix) Time in Seconds.
    end_unix : int
        Epoch (Unix) Time in Seconds.
    freq : str
        Frequency Used ('second', 'minute', 'hour', 'day').
    filename : str, optional
        File Path. The default is None.
    sub : bool, optional
        Whether to Find Submissions or Comments. The default is True.

    Returns
    -------
    reddit_vol : DataFrame
        Only returns if filename is None,
        otherwise print to a .csv file at filename.

    """
    if filename is not None:
        if os.stat(filename).st_size == 0:  # If the file is blank
            last_start_unix = None
        else:  # Otherwise set the last start_unix date
            last_start_unix = pd.read_csv(filename, index_col='Date').index[
                -1]
            last_start_unix = ts_to_unix(last_start_unix)
        # Set the start_unix date of our function as the last start_unix
        if last_start_unix is not None and start_unix < last_start_unix:
            start_unix = last_start_unix

    dfs_reddit_vol = []
    if sub is True:
        url = 'https://api.pushshift.io/reddit/search/submission/'
    else:
        url = 'https://api.pushshift.io/reddit/search/comment/'

    for subreddit in subreddits:
        parameters = {
            'subreddit': subreddit,
            'size': 0,
            'after': start_unix,
            'before': end_unix,
            'aggs': 'created_utc',
            'frequency': freq,
        }
        response = requests.get(url=url, params=parameters)
        print(response.url)
        df_reddit_vol = pd.DataFrame(response.json()['aggs']['created_utc'])
        dfs_reddit_vol.append(df_reddit_vol)

    reddit_vol = pd.DataFrame(columns=['count', 'date'])
    reddit_vol['count'] = dfs_reddit_vol[0]['doc_count'] + dfs_reddit_vol[1][
        'doc_count']
    reddit_vol['date'] = dfs_reddit_vol['key']
    reddit_vol['date'] = pd.to_datetime(reddit_vol['date'], unit='s')
    reddit_vol = reddit_vol.set_index('date')

    if filename is not None:
        reddit_vol.to_csv(filename)
    else:
        return reddit_vol


# Temporarily Disabled by Pushshift
def get_total_volume(subreddits, start_unix, end_unix, freq,
                     file_name=None):
    """
    Get total number of Reddit Submissions & Comments.

    Parameters
    ----------
    subreddits : list
        List of Targeted Subreddits.
    start_unix : int
        Time in Unix form.
    end_unix : int
        Time in Unix form.
    freq : str
        Frequency Used ('second', 'minute', 'hour', 'day').
    file_name : str, optional
        File Path. The default is None.

    Returns
    -------
    reddit_vol : DataFrame
        Only returns if filename is None,
        otherwise print to a .csv file to file_name.

    """
    reddit_volsub = get_volume(start_unix, end_unix, freq, subreddits)
    reddit_volcmt = get_volume(start_unix, end_unix, freq, subreddits,
                               sub=False)

    reddit_vol = pd.merge(reddit_volsub, reddit_volcmt,
                          left_index=True, right_index=True,
                          suffixes=['_sub', '_cmt'])
    reddit_vol['count'] = reddit_vol['count_cmt'] + reddit_vol['count_sub']

    if file_name is not None:
        reddit_vol.to_csv(file_name)
    else:
        return reddit_vol
