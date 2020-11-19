import pandas as pd
from SentimentAnalysis.pre_process import pre_process
from SentimentAnalysis.sentiment_score import sentiment

### Stocktwits Tweets Processing ###
stocktwits = pd.read_csv("data/stocktwits.csv", index_col = 0)
# convert date in RFC3339 format to pd.Period (freq = 'D')
stocktwits['date'] = pd.to_datetime(stocktwits['datetime']).dt.to_period("D")
# pre-process text
stocktwits['processed'] = stocktwits['message'].apply(pre_process)
# compute sentiment
stocktwits['CL sentiment'] = stocktwits['processed'].apply(sentiment)
# compute average sentiment of each day
stocktwits_sent = stocktwits.groupby('date')['CL sentiment'].mean()
# count messages of each day
stocktwits_volume = stocktwits.groupby('date')['message_id'].count()
stocktwits_volume = stocktwits_volume.rename('volume')
# convert Period to pd.Timestamp (for plotting with crix later)
stocktwits_sent.index = stocktwits_sent.index.to_timestamp()
stocktwits_volume.index = stocktwits_volume.index.to_timestamp()
# export for later usage
stocktwits_sent.to_csv("data/direct/stocktwits_sentiment.csv")
stocktwits_volume.to_csv("data/direct/stocktwits_volume.csv")

### Reddit Submissions Processing ###
reddit_sub = pd.read_csv("data/reddit_submissions.csv", index_col = 0)
# convert date in unix format to pd.Period (freq = 'D')
reddit_sub['date'] = pd.to_datetime(reddit_sub['created_utc'], 
                                    unit = 's').dt.to_period("D")
# data cleaning
reddit_sub.dropna(subset=['title'], inplace=True)
reddit_sub['content'].fillna('', inplace = True)
# merge two columns into a 'message' column
reddit_sub['message'] = reddit_sub['title'] + ' ' + reddit_sub['content']
# pre-process text
reddit_sub['processed'] = reddit_sub['message'].apply(pre_process)
# compute sentiment
reddit_sub['CL sentiment'] = reddit_sub['processed'].apply(sentiment)
# compute average sentiment of each day
reddit_sub_sent = reddit_sub.groupby('date')['CL sentiment'].mean()
# count messages of each day
reddit_sub_vol = reddit_sub.groupby('date')['id'].count()
reddit_sub_vol = reddit_sub_vol.rename('volume')
# convert Period to pd.Timestamp (for plotting with crix later)
reddit_sub_sent.index = reddit_sub_sent.index.to_timestamp()
reddit_sub_vol.index = reddit_sub_vol.index.to_timestamp()
# export for later usage
reddit_sub_sent.to_csv("data/direct/reddit_submissions_sentiment.csv")
reddit_sub_vol.to_csv("data/direct/reddit_submissions_volume.csv")

## Reddit Comments Processing ###
reddit_com = pd.read_csv("data/reddit_comments.csv", index_col = 0)
# convert date in unix format to pd.Period (freq = 'D')
reddit_com['date'] = pd.to_datetime(reddit_com['created_utc'], 
                                    unit = 's').dt.to_period("D")
# data cleaning
reddit_com['content'].fillna('', inplace = True)
index_deleted = reddit_com[reddit_com['content'] == '[deleted]'].index
index_removed = reddit_com[reddit_com['content'] == '[removed]'].index
reddit_com.drop(index_deleted, inplace = True)
reddit_com.drop(index_removed, inplace = True)

# pre-process text
reddit_com['processed'] = reddit_com['content'].apply(pre_process)
# compute sentiment
reddit_com['CL sentiment'] = reddit_com['processed'].apply(sentiment)
# compute average sentiment of each day
reddit_com_sent = reddit_com.groupby('date')['CL sentiment'].mean()
# count messages of each day
reddit_com_vol = reddit_com.groupby('date')['id'].count()
reddit_com_vol = reddit_com_vol.rename('volume')
# convert Period to pd.Timestamp (for plotting with crix later)
reddit_com_sent.index = reddit_com_sent.index.to_timestamp()
reddit_com_vol.index = reddit_com_vol.index.to_timestamp()
# export for later usage
reddit_com_sent.to_csv("data/direct/reddit_comments_sentiment.csv")
reddit_com_vol.to_csv("data/direct/reddit_comments_volume.csv")
