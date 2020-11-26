"""Run package src.process in cmd line.

The package src.process performs text process and sentiment analysis
on StockTwits & Reddit text data. It also counts the total number of messages
on each platform and use those as a sentiment indicator. At the end,
the package organizes all dataseries into a final dataset ready to be fitted
in our model.
"""
import warnings

import pandas as pd

from . import gather_data
from .sentiment_score import sentiment
from .text_process import text_process

if __name__ == '__main__':
    warnings.simplefilter(action='ignore', category=FutureWarning)
    warnings.filterwarnings(action='ignore', category=UserWarning)
    # 1. StockTwits Tweets
    stocktwits = pd.read_csv("data/01_raw/stocktwits.csv", index_col=0)
    # Convert date in RFC3339 format to pd.Period (freq = 'D')
    stocktwits['date'] = pd.to_datetime(stocktwits['datetime']).dt.to_period(
        "D")
    # Text process
    stocktwits['processed'] = stocktwits['message'].apply(text_process)
    # Compute sentiment
    stocktwits['CL sentiment'] = stocktwits['processed'].apply(sentiment)
    # Compute average sentiment of each day
    stocktwits_sent = stocktwits.groupby('date')['CL sentiment'].mean()
    # Count messages of each day
    stocktwits_volume = stocktwits.groupby('date')['message_id'].count()
    stocktwits_volume = stocktwits_volume.rename('volume')
    # Convert period to pd.Timestamp (for graphing later with plotly)
    stocktwits_sent.index = stocktwits_sent.index.to_timestamp()
    stocktwits_volume.index = stocktwits_volume.index.to_timestamp()
    # Export
    stocktwits_sent.to_csv("data/02_processed/direct/stocktwits_sentiment.csv")
    stocktwits_volume.to_csv("data/02_processed/direct/stocktwits_volume.csv")

    # 2. Reddit Submissions Processing #
    reddit_sub = pd.read_csv("data/01_raw/reddit_submissions.csv", index_col=0)
    # Convert date in unix format to pd.Period (freq = 'D')
    reddit_sub['date'] = pd.to_datetime(reddit_sub['created_utc'],
                                        unit='s').dt.to_period("D")
    # Clean NA
    reddit_sub.dropna(subset=['title'], inplace=True)
    reddit_sub['content'].fillna('', inplace=True)
    # Merge two columns 'title' & 'content' into a 'message' column
    reddit_sub['message'] = reddit_sub['title'] + ' ' + reddit_sub['content']
    # Text process
    reddit_sub['processed'] = reddit_sub['message'].apply(text_process)
    # Compute sentiment
    reddit_sub['CL sentiment'] = reddit_sub['processed'].apply(sentiment)
    # Compute average sentiment of each day
    reddit_sub_sent = reddit_sub.groupby('date')['CL sentiment'].mean()
    # Count messages of each day
    reddit_sub_vol = reddit_sub.groupby('date')['id'].count()
    reddit_sub_vol = reddit_sub_vol.rename('volume')
    # Convert Period to pd.Timestamp (for graphing later with plotly)
    reddit_sub_sent.index = reddit_sub_sent.index.to_timestamp()
    reddit_sub_vol.index = reddit_sub_vol.index.to_timestamp()
    # Export
    reddit_sub_sent.to_csv(
        "data/02_processed/direct/reddit_submissions_sentiment.csv")
    reddit_sub_vol.to_csv(
        "data/02_processed/direct/reddit_submissions_volume.csv")

    # 3. Reddit Comments Processing #
    reddit_com = pd.read_csv("data/01_raw/reddit_comments.csv", index_col=0)
    # Convert date in unix format to pd.Period (freq = 'D')
    reddit_com['date'] = pd.to_datetime(reddit_com['created_utc'],
                                        unit='s').dt.to_period("D")
    # Data cleaning
    reddit_com['content'].fillna('', inplace=True)
    index_deleted = reddit_com[reddit_com['content'] == '[deleted]'].index
    index_removed = reddit_com[reddit_com['content'] == '[removed]'].index
    reddit_com.drop(index_deleted, inplace=True)
    reddit_com.drop(index_removed, inplace=True)
    # Text process
    reddit_com['processed'] = reddit_com['content'].apply(text_process)
    # Compute sentiment
    reddit_com['CL sentiment'] = reddit_com['processed'].apply(sentiment)
    # Compute average sentiment of each day
    reddit_com_sent = reddit_com.groupby('date')['CL sentiment'].mean()
    # Count messages of each day
    reddit_com_vol = reddit_com.groupby('date')['id'].count()
    reddit_com_vol = reddit_com_vol.rename('volume')
    # Convert Period to pd.Timestamp (for plotting with crix later)
    reddit_com_sent.index = reddit_com_sent.index.to_timestamp()
    reddit_com_vol.index = reddit_com_vol.index.to_timestamp()
    # Export
    reddit_com_sent.to_csv(
        "data/02_processed/direct/reddit_comments_sentiment.csv")
    reddit_com_vol.to_csv(
        "data/02_processed/direct/reddit_comments_volume.csv")

    # 4. Gather Data #
    gather_data.run()
