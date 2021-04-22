#!/usr/bin/env python3
"""Getting Messages From StockTwits and Reddit

Run in the terminal: `python -m src.data`.
"""
import pandas as pd

from . import stocktwits, reddit, others
from .convert_ts import ts_to_unix

if __name__ == '__main__':
    # Get StockTwits messages
    start = '2014-11-28 00:00:00'
    end = '2021-03-10 00:00:00'
    st_cashtag = pd.read_csv('data/00_external/symbols.csv', header=None)[1]
    symbols = st_cashtag[st_cashtag.str.endswith('.X')].to_list()

    for symbol in symbols:
        try:
            stocktwits.get_tweets(symbol, start, end,
                                  file_name=f"data/01_raw/stocktwits/"
                                            f"{symbol[:-2]}.csv")
        except IndexError:
            print(f"No tweet with {symbol} exists on StockTwits.")
            print("------------")
    print(
        f"Combining files containing tweets with a single cashtag to one "
        f"master file...")
    print("------------")
    combined_csv = pd.concat(
        [pd.read_csv(f"data/01_raw/stocktwits/{symbol[:-2]}.csv") for symbol in
         symbols], ignore_index=True)
    combined_csv.to_csv("data/01_raw/stocktwits.csv")

    # Get Reddit comments & submissions
    subreddits = ['Bitcoin', 'CryptoCurrency']
    start_unix = ts_to_unix(start)
    end_unix = ts_to_unix(end)

    for subreddit in subreddits:
        reddit.get_comments(subreddit, start_unix, end_unix,
                            file_name=f"data/01_raw/reddit/comments_"
                                      f"{subreddit}.csv")
        reddit.get_submissions(subreddit, start_unix, end_unix,
                               file_name=f"data/01_raw/reddit/submissions_"
                                         f"{subreddit}.csv")

    # Get trade volume
    others.get_trade_volume(start_unix, end_unix,
                            file_name=f'data/02_processed/indirect'
                                      f'/trade_volume.csv')

    # Get daily Google Trends
    others.get_google_trends('bitcoin', start_unix, end_unix,
                             file_name=f'data/02_processed/indirect'
                                       f'/google_trends.csv')
