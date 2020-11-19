import pandas as pd

start = pd.Timestamp('2014-11-28 00:00:00')
end = pd.Timestamp('2020-07-25 00:00:00')

## Get Trading Volume
import requests
url = 'https://api.nomics.com/v1/volume/history'

start_RFC3339  =  start.strftime('%Y-%m-%dT') +  '00:00:00Z'
end_RFC3339 = end.strftime('%Y-%m-%dT') +  '00:00:00Z'

parameters = {
    'key' : 'e729d9cb5041a06c2a839122e0994bfe',
    'start' : start_RFC3339,
    'end' : end_RFC3339,
    }
response = requests.get(url = url, params = parameters)
trade_volume = pd.DataFrame(response.json())
trade_volume = trade_volume.set_index('timestamp')
trade_volume.index = pd.to_datetime(trade_volume.index)
trade_volume.index = trade_volume.index.tz_convert(None)
trade_volume.to_csv('data/indirect/trade_volume.csv')

## Get Google Trends Data
from pytrends import dailydata

search_volume = dailydata.get_daily_data('bitcoin', 2014, 11, 2020, 7, geo = '')
search_volume = search_volume.drop(['bitcoin_unscaled', 'bitcoin_monthly', 
                                    'scale', 'isPartial'], axis = 1)
search_volume.to_csv('data/indirect/google_volume.csv')

## Get FT headlines ##
from bs4 import BeautifulSoup
import re

def get_ft_headlines(kw = 'bitcoin', start = '2014-11-15', end = '2020-07-27'):
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
    
        headlines_soup = ft_soup.findAll("button",{"class":"n-myft-ui__button"})
        if headlines_soup == []:
            print("Finished!")
            data_df = pd.DataFrame(data, columns = ['headline', 'date'])
            break
        headlines = []
        for headline in headlines_soup:
            text = headline['title']
            text = re.sub(r'^Save\s','', text)
            text = re.sub(r'\s?\sto\smyFT\sfor\slater$','', text)
            headlines.append(text)
    
        dates_soup = ft_soup.findAll("div", {"class":"o-teaser__timestamp"})
        dates = []
        for date in dates_soup:
            dates.append(date.time['datetime'][:10])
        
        page_data = list(zip(headlines, dates))
        data += page_data
        print(f"Done page {page+loop}!")
        page += 1
    
        last_date = pd.Timestamp(dates[-1][:10])
        if page > 40 and last_date > pd.Timestamp(start):
            end = last_date
            page = 1
            loop += 40

    return data_df
    