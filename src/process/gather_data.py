#!/usr/bin/env python3
"""Gather features chosen for our model into a final dataset

The final dataset is stored at "data/02_processed/final_dataset.csv".
"""
import pandas as pd


def run():
    """
    Runs the module.

    Returns
    -------
    NoneType
        None.
    """
    
    # Market Return: Crix #
    crix = pd.read_json('data/02_processed/crix.json')
    crix.set_index('date', inplace=True)
    crix = crix.rename(columns={'price': 'CRIX'})

    # Direct Sentiment Measures #
    direct = ['stocktwits_sentiment', 'reddit_submissions_sentiment',
              'reddit_comments_sentiment']
    direct_files = [f"data/02_processed/direct/{measure}.csv" for measure in
                    direct]

    # 1 - Stocktwits Tweets Sentiment
    stocktwits_sent = pd.read_csv(direct_files[0], index_col='date')
    stocktwits_sent = stocktwits_sent.rename(columns={
        'CL sentiment': 'Stocktwits Sent'})

    # 2 - Reddit Submissions Sentiment
    reddit_sub_sent = pd.read_csv(direct_files[1], index_col='date')
    reddit_sub_sent = reddit_sub_sent.rename(columns={
        'CL sentiment': 'Reddit Posts Sent'})

    # 3 - Reddit Comments Sentiment
    reddit_com_sent = pd.read_csv(direct_files[2], index_col='date')
    reddit_com_sent = reddit_com_sent.rename(columns={
        'CL sentiment': 'Reddit Comments Sent'})

    direct_measures = [stocktwits_sent, reddit_sub_sent, reddit_com_sent]

    # Indirect Sentiment Measures #
    indirect = ['vcrix', 'trade_volume', 'google_trends', 'stocktwits_volume',
                'reddit_submissions_volume', 'reddit_comments_volume']
    indirect_files = [f'data/02_processed/indirect/{measure}.csv' for measure
                      in indirect]

    # 1 - VCRIX
    vcrix = pd.read_csv(indirect_files[0], index_col='date')

    # 2 - Daily Trading Volume
    trade_volume = pd.read_csv(indirect_files[1], index_col='Date')

    # 3 - Google Search Volume
    google_trend = pd.read_csv(indirect_files[2], index_col='Date')

    # 4 - Stocktwits Tweets Volume
    stocktwits_volume = pd.read_csv(indirect_files[3], index_col='date')
    stocktwits_volume = stocktwits_volume.rename(columns={
        'volume': 'Stocktwits Volume'})

    # 5 - Reddit Submissions Volume
    reddit_sub_volume = pd.read_csv(indirect_files[4], index_col='date')
    reddit_sub_volume = reddit_sub_volume.rename(columns={
        'volume': 'Posts Volume'})

    # 6 - Reddit Comments Volume
    reddit_com_volume = pd.read_csv(indirect_files[5], index_col='date')
    reddit_com_volume = reddit_com_volume.rename(columns={
        'volume': 'Comments Volume'})

    indirect_measures = [vcrix, trade_volume, google_trend,
                         stocktwits_volume, reddit_sub_volume,
                         reddit_com_volume]

    # Final dataset #
    list_datasets = [crix] + direct_measures + indirect_measures
    for data in list_datasets:
        data.index = pd.to_datetime(data.index)
    final_dataset = pd.concat(list_datasets, axis=1, join='inner')
    final_dataset.index.name = 'Date'
    final_dataset.to_csv('data/02_processed/final_dataset.csv',)
