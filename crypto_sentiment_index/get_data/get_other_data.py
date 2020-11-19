#!/usr/bin/env python3
"""Get the Dataseries of Other Features.

This module defines the functions that download the dataseries of: crypto 
daily (global, market-aggregated) trading volume, Google Trends, Financial
Times headlines related to cryptocurrencies.
"""
import pandas as pd
import requests

import crypto_sentiment_index.get_data.convert_ts as convert


# Get trading volume

def get_trade_vol(start_unix, end_unix, filename):
    """
    Download crypto daily (global, market-aggregated) trading volume using
    Nomics API.

    Parameters
    ----------
    start_unix : int
        Epoch (Unix) Time in Seconds.
    end_unix : int
        Epoch (Unix) Time in Seconds.
    filename : str
        File path.

    Returns
    -------
    NoneType
        None.
    """

    url = 'https://api.nomics.com/v1/volume/history'

    start = convert.unix_to_ts(start_unix)
    end = convert.unix_to_ts(end_unix)
    start_rfc3339 = start.strftime('%Y-%m-%dT') + '00:00:00Z'
    end_rfc3339 = end.strftime('%Y-%m-%dT') + '00:00:00Z'

    parameters = {
        'key': 'e729d9cb5041a06c2a839122e0994bfe',
        'start': start_rfc3339,
        'end': end_rfc3339,
    }
    response = requests.get(url=url, params=parameters)
    if response.status_code != 200:
        print(f"Response Status: {response.status_code}")

    hist_vol = pd.DataFrame(response.json())
    hist_vol.rename({'timestamp': 'Date', 'volume': 'Market Volume'},
                    axis=1, inplace=True)
    hist_vol['Date'] = hist_vol['Date'].apply(convert.remove_tz)
    hist_vol = hist_vol.set_index('Date')
    hist_vol.to_csv(filename)


# Get Google Trends data
from pytrends import dailydata

search_volume = dailydata.get_daily_data('bitcoin', 2014, 11, 2020, 7, geo='')
search_volume = search_volume.drop(['bitcoin_unscaled', 'bitcoin_monthly',
                                    'scale', 'isPartial'], axis=1)
search_volume.to_csv('data/indirect/google_volume.csv')

# Get FT headlines
from bs4 import BeautifulSoup
import re


def get_ft_headlines(kw='bitcoin', start='2014-11-15', end='2020-07-27'):
    """
    Search for Financial Times headlines containing keywords.
    
    Parameters
    ----------
    kw : str, optional
        Keywords to be searched for. The default is 'bitcoin'.
    start : str, optional
        Start date of the search (YYYY-MM-DD). The default is '2014-11-15'.
    end : TYPE, optional
        End date of the search (YYYY-MM-DD). The default is '2020-07-27'.

    Returns
    -------
    data_df : DataFrame
        DataFrame containing 2 columns: headline & posted date.

    """
    url_base = f'https://www.ft.com/search?q={kw}'
    data = []
    page = 1
    loop = 0
    while True:
        url = (f"{url_base}&"
               f"page={page}&"
               f"contentType=article&"
               f"dateTo={end}&dateFrom={start}&"
               f"sort=date&expandRefinements=true"
               )
        response = requests.get(url)
        ft_soup = BeautifulSoup(response.content, 'html')

        headlines_soup = ft_soup.findAll("button",
                                         {"class": "n-myft-ui__button"})
        if not headlines_soup:
            print("Finished!")
            data_df = pd.DataFrame(data, columns=['headline', 'date'])
            break
        headlines = []
        for headline in headlines_soup:
            text = headline['title']
            text = re.sub(r'^Save\s', '', text)
            text = re.sub(r'\s?\sto\smyFT\sfor\slater$', '', text)
            headlines.append(text)

        dates_soup = ft_soup.findAll("div", {"class": "o-teaser__timestamp"})
        dates = []
        for date in dates_soup:
            dates.append(date.time['datetime'][:10])

        page_data = list(zip(headlines, dates))
        data += page_data
        print(f"Done page {page + loop}!")
        page += 1

        last_date = pd.Timestamp(dates[-1][:10])
        if page > 40 and last_date > pd.Timestamp(start):
            end = last_date
            page = 1
            loop += 40

    return data_df
