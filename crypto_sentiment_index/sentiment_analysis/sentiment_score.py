import nltk
import pandas as pd

sent_lexicon = pd.read_csv('data/lexicon/crypto_lexicon.csv')
sent_score = sent_lexicon[['keyword','sw']]

unigram_score = sent_score[sent_score['keyword'].apply(
    lambda text: len(text.split())) == 1]

bigram_score = sent_score[sent_score['keyword'].apply(
    lambda text: len(text.split())) == 2]

pd.options.mode.chained_assignment = None
bigram_score['keyword'] = bigram_score['keyword'].apply(
    lambda text: tuple(text.split()))

unigram_dict = unigram_score.set_index('keyword').to_dict()
bigram_dict = bigram_score.set_index('keyword').to_dict()

def sentiment(text):
    count, sent = 0, 0
    uni_tokens = text.split()
    bi_tokens = list(nltk.ngrams(uni_tokens, 2))   
    for token in bi_tokens:
        try:
            sent += bigram_dict['sw'][token]
            count += 1
            for tok in token:
                uni_tokens.remove(tok)       
        except Exception:
            pass
        
    for token in uni_tokens:
        try:
            sent += unigram_dict['sw'][token]
            count += 1
        except Exception:
            pass    
        
    if count != 0:
        sent /= count
        
    return sent      
