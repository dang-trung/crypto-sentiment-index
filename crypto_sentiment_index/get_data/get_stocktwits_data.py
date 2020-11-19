"""
    EXTRACT DATA FROM STOCKTWITS API
    WORKAROUND RATE LIMITS USING PROXY
    CHANGED WORKAROUND METHOD TO USING MULTIPLE ACCESS KEYS
"""
import csv
import json
import os
import time
import requests
import pandas as pd

start = pd.Timestamp('2014-11-28 00:00:00')
end = pd.Timestamp('2020-07-25 00:00:00')

def get_stocktwits_data(symbol, start = "", end = "",
                        file_name = 'data//stocktwits_data.csv'):    
    fields = ['symbol', 'message', 'sentiment', 'datetime', 'user', 'message_id']
    token = 0
    base_url = 'https://api.stocktwits.com/api/2/streams/symbol/'
    
    access_token = ['', 'access_token=32a3552d31b92be5d2a3sd282ca3a864f96e95818&',
                    'access_token=44ae93a5279092f7804a0ee04753252cbf2ddfee&',
                    'access_token=990183ef04060336a46a80aa287f774a9d604f9c&']
    
    file = open(file_name, 'a', newline='', encoding='utf-8')
    start_date = pd.Timestamp(start, tz = 'UTC')
    end_date = pd.Timestamp(end, tz = 'UTC')
    
    # DETERMINE WHERE TO START IF RESUMING SCRIPT
    if os.stat(file_name).st_size == 0:
        # OPEN FILE IN APPEND MODE AND WRITE HEADERS TO FILE
        last_message_id = None
        csvfile = csv.DictWriter(file, fields)
        csvfile.writeheader()
    else:
        # FIRST EXTRACT LAST MESSAGE ID THEN OPEN FILE IN APPEND MODE WITHOUT WRITING HEADERS
        file = open(file_name, 'r', newline='', encoding='utf-8')
        csvfile = csv.DictReader((line.replace('\0', '') for line in file))
        data = list(csvfile)
        data = data[-1]
        last_message_id = data['message_id']
        file.close()
        file = open(file_name, 'a', newline='', encoding='utf-8')
        csvfile = csv.DictWriter(file, fields)
    
    # req_proxy = RequestProxy()
    
    stocktwit_url = (base_url + symbol + ".json?" + access_token[token])
    if last_message_id is not None:
        stocktwit_url += "max=" + str(last_message_id)
    
    api_hits = 0
    while True:
        # response = req_proxy.generate_proxied_request(stocktwit_url)
        try:
            response = requests.get(stocktwit_url)
        except Exception:
            response = None
    
        if response is not None:
    
            if response.status_code == 429:
                print("REQUEST IP RATE LIMITED FOR {} seconds.".format(
                    int(response.headers['X-RateLimit-Reset']) - int(time.time())))
    
            if not response.status_code == 200:
                stocktwit_url = (base_url + symbol + ".json?" + access_token[token] 
                                 + "max=" + str(last_message_id))
                token = (token + 1) % (len(access_token))
                continue
            
            reach_start_date = False
            api_hits += 1
            response = json.loads(response.text)
            last_message_id = response['cursor']['max']
            # WRITE DATA TO CSV FILE
            for message in response['messages']:
                # PREPARE OBJECT TO WRITE IN CSV FILE
                if pd.Timestamp(message['created_at']) < start_date:
                    reach_start_date = True
                elif pd.Timestamp(message['created_at']) > end_date:
                    pass
                else:
                    obj = {}
                    obj['symbol'] = symbol
                    obj['message'] = message['body']
                    if message['entities']['sentiment'] == None:
                        obj['sentiment'] = 'None'
                    else:
                        obj['sentiment'] = message['entities']['sentiment']['basic']
                    obj['datetime'] = message['created_at']
                    obj['user'] = message['user']['id']
                    obj['message_id'] = message['id']
                    csvfile.writerow(obj)
                    file.flush()
    
            print(f"API HITS: {api_hits} {symbol[:-2]}.")
    
            # NO MORE MESSAGES
            if not response['messages']:
                break
            if reach_start_date == True:
                break
    
        # ADD MAX ARGUMENT TO GET OLDER MESSAGES
        stocktwit_url = (base_url + symbol + ".json?" + access_token[token] 
                         + "max=" + str(last_message_id))
        token = (token + 1) % (len(access_token))
    
    file.close()

if __name__ == '__main__':
    st_cashtag = pd.read_csv('data//symbols.csv', header = None)
    st_cashtag = st_cashtag.drop(columns = [0, 3, 4])
    st_cashtag.columns = ['Cashtag', 'Desc']
    st_cashtag = st_cashtag[st_cashtag['Cashtag'].str.endswith('.X')]
    st_cashtag = st_cashtag.reset_index().drop('index', axis = 1)
    st_cashtag.iloc[0,1] = 'Bitcoin'
    symbols = st_cashtag['Cashtag'].to_list()
    start = "2014-11-28"
    end = "2020-07-26"
    for symbol in symbols[485:]:
        try:
            get_stocktwits_data(symbol = symbol, start = start, end = end,
                            file_name = f"data//stocktwits//{symbol[:-2]}.csv")