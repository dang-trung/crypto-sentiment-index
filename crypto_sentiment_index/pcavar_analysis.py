import pandas as pd

### Market Return: Crix ###
crix = pd.read_json('data/crix/crix.json')
crix = crix.set_index('date')
crix = crix.rename(columns={'price' : 'crix'})
start = crix.index[0]
end = crix.index[-1]

### Direct Sentiment Measures ###

direct = ['stocktwits_sentiment',  'reddit_submissions_sentiment', 
          'reddit_comments_sentiment', ]
direct_file = [f"data/direct/{measure}.csv" for measure in direct]

# 1 - Stocktwits Tweets Sentiment
stocktwits_sent = pd.read_csv(direct_file[0], index_col = 'date')
stocktwits_sent = stocktwits_sent.rename(columns = 
                                         {'CL sentiment' :'Stocktwits Sent'})

# 2 - Reddit Submissions Sentiment
reddit_sub_sent = pd.read_csv(direct_file[1], index_col = 'date')
reddit_sub_sent = reddit_sub_sent.rename(columns = 
                                         {'CL sentiment' :'Reddit Posts Sent'})
 
# 3 - Reddit Comments Sentiment
reddit_com_sent = pd.read_csv(direct_file[2], index_col = 'date')
reddit_com_sent = reddit_com_sent.rename(columns = 
                                         {'CL sentiment' :'Reddit Comments Sent'})

direct_measures = [stocktwits_sent, reddit_sub_sent, reddit_com_sent]

### Indirect Sentiment Measures ###
indirect = ['vcrix', 'trade_volume','google_volume','stocktwits_volume', 
            'reddit_submissions_volume','reddit_comments_volume']
indirect_files = [f'data/indirect/{measure}.csv' for measure in indirect]

# 1 - VCRIX
vcrix = pd.read_csv(indirect_files[0], index_col = 'date')

# 2 - Daily Trading Volume
trade_volume = pd.read_csv(indirect_files[1], index_col = 'timestamp')

# 3 - Google Search Volume
google_volume = pd.read_csv(indirect_files[2], index_col = 'date')

# 4 - Stocktwits Tweets Volume
stocktwits_volume = pd.read_csv(indirect_files[3], index_col = 'date')
stocktwits_volume = stocktwits_volume.rename(columns = 
                                         {'volume' :'Stocktwits Volume'})

# 5 - Reddit Submissions Volume
reddit_sub_volume = pd.read_csv(indirect_files[4], index_col = 'date')
reddit_sub_volume = reddit_sub_volume.rename(columns = 
                                         {'volume' :'Posts Volume'})

# 6 - Reddit Comments Volume
reddit_com_volume = pd.read_csv(indirect_files[5], index_col = 'date')
reddit_com_volume = reddit_com_volume.rename(columns = 
                                         {'volume' :'Comments Volume'})

indirect_measures = [vcrix, trade_volume, google_volume,
                     stocktwits_volume, reddit_sub_volume,
                     reddit_com_volume]

### Summary data ###
list_data = [crix] + direct_measures + indirect_measures
for data in list_data:
    data.index = pd.to_datetime(data.index)
data = pd.concat(list_data, axis = 1, join = 'inner')

### Plot with CRIX ### 
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.io as pio

def plotcrix(data, one = 'crix', two = '', name1 = '', name2 = ''):
    pio.renderers.default = 'browser'
    default_layout = go.Layout(font_family = ('Gravitas One'),
                           xaxis_showgrid = False,
                           yaxis_showgrid = False,
                           showlegend = True,
                           legend_orientation = 'h',
                           legend_yanchor = 'bottom',
                           legend_y = 1,
                           legend_xanchor = 'center',
                           legend_x = 0.5)    
    trace_main = go.Scatter(x = data.index, y = data[one], name = name1, 
                           marker_color = '#FF6E58')
    if two != "":
       fig = make_subplots(rows = 1, cols = 1, shared_xaxes = True, 
                    specs = [[{'secondary_y' : True}]])
       
       trace_sub = go.Scatter(x = data.index, y = data[two], 
                           name = name2, marker_color = '#21CCCB')
       fig.add_trace(trace_main, secondary_y = False)
       fig.add_trace(trace_sub, secondary_y = True)
       fig['layout']['yaxis2']['showgrid'] = False
       fig.update_layout(default_layout)
       
    else:
       fig = go.Figure(trace_main, default_layout)
       
    fig.show()
    
if __name__ == '__main__':
    
    from sklearn.decomposition import PCA
    from sklearn.preprocessing import StandardScaler
    
    features = data.columns[1:].to_list() # choose columns
    x = data.loc[:, features].values # choose data
    x = StandardScaler().fit_transform(x) # standardized
    pca = PCA(n_components=1) 
    principalComponents = pca.fit_transform(x) # pca
    principal_df = pd.DataFrame(data = principalComponents
             , columns = ['Sent'])
    principal_df.index = data.index
    crix_pca = pd.concat([crix, principal_df], axis = 1, join = 'inner')
    crix_pca
    plotcrix(data = crix_pca, one ='crix', two = 'Sent', name1 = '$CRIX$', name2 = '$SENT$')
    pca.explained_variance_ratio_ # explained ratio
    pca.components_ # loading scores
    
    from statsmodels.tsa.api import VAR
    from statsmodels.tsa.stattools import adfuller, kpss
    
    crix_pca['ret'] = (crix_pca['crix'].diff() / crix_pca['crix'].shift(1))
    crix_pca['delta Sent'] = crix_pca['Sent'].diff()
    crix_pca.dropna(inplace=True)
    # crix_pca.index = crix_pca.index.to_period('D')
    
# stationarity test

    for col in ["crix", "Sent", "ret", "delta Sent"]:
        X = crix_pca[col].values
        result = adfuller(X)
        result2 = kpss(X)
        print('--------')
        print(col)
        print('ADF Statistic: %f' % result[0])
        print('p-value: %f' % result[1])
        print('Critical Values:')
        for key, value in result[4].items():
            print('\t%s: %.3f' % (key, value))
        
        if result[0] < result[4]["5%"]:
            print ("Reject Ho - Time Series is Stationary")
        else:
            print ("Failed to Reject Ho - Time Series is Non-Stationary")
        
        print(f'KPSS Statistic: {result2[0]}')
        print('p-value: {result2[0]}')

# VAR
    model = VAR(crix_pca.loc[:,['ret','delta Sent']])
    results = model.fit(maxlags = 15, ic = 'bic')
    results.summary()
    results.irf().plot()
    
# trading strategy
    pred_ret = results.fittedvalues['ret']
    def signal(num):
        if num > 0:
            return 1
        elif num < 0:
            return -1
        else:
            return 0
    crix_pca['signal'] = pred_ret.apply(signal)
    crix_pca['Cum Market Ret'] = (crix_pca['ret'] + 1).cumprod()
    crix_pca['Cum Strategy Ret'] =(crix_pca['ret']*crix_pca['signal'] + 1).cumprod()
    crix_pca.loc[:,['Cum Market Ret','Cum Strategy Ret']].plot()
