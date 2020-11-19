import re
import html
import string
import pandas as pd

# Repeated chars more than 3 times
repeat_regex = r'(\w)\1{2,}' 
# Cashtag: $<word><opt .-><opt word>
cashtag_regex = r'\$\w+[.-]?\w?' 
# Money: <$ or €><digits><opt word>
moneytag_regex = r'[\$€]\d+\w?' 
# Numbers: <1 or more nums>
numbertag_regex = r'\d+[\.,]?\d?\w?' 
# Hyperlinks: http<opt s>://<opt www.><words><. words><opt />     
linktag_regex = r'https?://(www\.)?(\w+)(\.\w+)/?' 
# Users: @<opt words>
usertag_regex = r'@\w+'

# Remove stopwords
stops = pd.read_csv('data//stopwords.csv', header = None)[0].to_list()
stop_set = '|'.join(stops)
stop_regex = rf"\b({stop_set})\s"

# Negative words
negs = pd.read_csv('data//negative.csv', header = None)[0].to_list()
neg_set = '|'.join(negs)
negtag_regex = rf"({neg_set})\s(\w?)"

# Remove punctuations
punctuation = string.punctuation
punctuation = punctuation.replace('!', '')
punctuation = punctuation.replace('?', '')
punctuation = punctuation.replace("'", '')
punc_regex = rf"[{punctuation}]"

def pre_process(text):
    text = text.lower()    # Lowercase
    text = html.unescape(text) # Convert html codes to normal strings
    text = re.sub(repeat_regex, r'\1\1\1',text)
    text = re.sub(cashtag_regex,'cashtag', text)
    text = re.sub(moneytag_regex,'moneytag', text)
    text = re.sub(numbertag_regex,'numbertag', text)
    text = re.sub(linktag_regex,'linktag', text)
    text = re.sub(usertag_regex,'usertag', text)    
    text = re.sub(stop_regex, '', text)
    text = re.sub(punc_regex, '', text)    
    text = re.sub(negtag_regex,r' negtag_\2', text)
    text = re.sub(r"'", '', text)
    
    return text
    
    
    
    
    
    
    
    
    
    