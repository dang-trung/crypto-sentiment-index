"""Score sentiment of text messages.

This module defines the function score sentiment based on the
crypto-specific lexicon created by Chen et al. (2019).
"""
import nltk
import pandas as pd

sent_lexicon = pd.read_csv('data/00_external/crypto_lexicon.csv')
sent_score = sent_lexicon[['keyword', 'sw']]

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
    """
    Score the sentiment of a sentence.

    Parameters
    ----------
    text : str
        Input sentence (preferably already cleaned by the function
                        text_process).

    Returns
    -------
    sent : int
        Sentiment score of the sentence.
        Lexicon used: Crypto-specific (Chen et al., 2019).

    """
    count, sent = 0, 0
    uni_tokens = text.split()
    bi_tokens = list(nltk.ngrams(uni_tokens, 2))
    for token in bi_tokens:
        try:
            sent += bigram_dict['sw'][token]
            count += 1
            for tok in token:
                uni_tokens.remove(tok)
        except (KeyError, ValueError):
            pass

    for token in uni_tokens:
        try:
            sent += unigram_dict['sw'][token]
            count += 1
        except (KeyError, ValueError):
            pass

    if count != 0:
        sent /= count

    return sent
