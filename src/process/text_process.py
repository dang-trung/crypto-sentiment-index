#!/usr/bin/env python3
"""Clean text messages.

This module defines the function to clean text messages so that only
information relevant to our sentiment analysis remains.
"""
import html
import re
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
stops = pd.read_csv('data/00_external/stopwords.csv', header=None)[0].to_list()
stop_set = '|'.join(stops)
stop_regex = rf"\b({stop_set})\s"

# Negative words
negs = pd.read_csv('data/00_external/negative.csv', header=None)[0].to_list()
neg_set = '|'.join(negs)
negtag_regex = rf"({neg_set})\s(\w?)"

# Remove punctuations
punctuation = string.punctuation
punctuation = punctuation.replace('!', '')
punctuation = punctuation.replace('?', '')
punctuation = punctuation.replace("'", '')
punc_regex = rf"[{punctuation}]"


def text_process(text):
    """
    Clean messages for sentiment analysis, based on rules inspired by
    Chen et al. (2019).

    Parameters
    ----------
    text : str
        Texts to be processed.

    Returns
    -------
    text : str
        Clean version of input texts.

    """
    text = text.lower()  # Lowercase
    text = html.unescape(text)  # Convert html codes to normal strings
    text = re.sub(repeat_regex, r'\1\1\1', text)
    text = re.sub(cashtag_regex, 'cashtag', text)  # Remove cashtags
    text = re.sub(moneytag_regex, 'moneytag', text)  # Remove moneytag
    text = re.sub(numbertag_regex, 'numbertag', text)  # Remove numbers
    text = re.sub(linktag_regex, 'linktag', text)  # Remove links
    text = re.sub(usertag_regex, 'usertag', text)  # Remove usertags
    text = re.sub(stop_regex, '', text)  # Remove stopwords
    text = re.sub(punc_regex, '', text)  # Remove punctuation
    text = re.sub(negtag_regex, r' negtag_\2', text)  # Negative words
    text = re.sub(r"'", '', text)

    return text
