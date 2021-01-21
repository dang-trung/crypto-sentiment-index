[![MIT License][license-shield]][license-url]
[![GitHub][github-shield]][github-url]
[![LinkedIn][linkedin-shield]][linkedin-url]

<!-- PROJECT LOGO -->
<br />
<p align="center">
  <a href="https://github.com/dang-trung/crypto-sentiment-index">
    <img src="https://raw.githubusercontent.com/othneildrew/Best-README-Template/master/images/logo.png" alt="Logo" width="80" height="80">
  </a>

  <h3 align="center">A Composite Sentiment Index for the Cryptocurrency Market</h3>
</p>
  <p align="center">
    Sentiment Measurement & Return Predictability.
  </p>

## Project Description
### Introduction

* **Objective**: Master's Degree Graduation Thesis.

* **Abstract**: Constructed a comprehensive list of 9 sentiment indicators in crypto market and combined these indicators into one single sentiment index. Proved the index to be an excellent predictor of crypto market returns using VAR models and Granger-Causality tests.

* **Status**: Completed

### Methods Used
* Sentiment Analysis (Utilizing a crypto-specific lexicon created by [Chen et al, 2019](dx.doi.org/10.2139/ssrn.3398423))
* Principal Component Analysis
* Vector Autoregression Models

### Dependencies
* Python 3
* numpy==1.18.5
* pandas==1.0.5
* scikit-learn==0.23.2
* pytrends==4.7.3
* statsmodels==0.12.0
* plotly==4.9.0
* nltk==3.5
* beautifulsoup4==4.9.3

### Interesting Results to Keep You Reading
* It is the **first time** (to my knowledge) that one follows a composite approach to create a sentiment index for the cryptocurrency market (i.e. combining multiple sentiment indicators into one index, the idea is to create an index that could remains stable and useful for a long period of time, according to [Brown & Cliff, 2004](https://doi.org/10.1016/j.jempfin.2002.12.001))
* The VAR model shows that the lagged values of my sentiment index are **significantly correlated** with the daily returns of the crypto market (at lag 1, 3, 4, 5).
* Granger-Causality tests show that the sentiment index is an **excellent predictor** of cryptocurrency returns.
* Over a period of 5+ years (12/2014 - 07/2020), a sentiment-based trading strategy was backtested and generated a portfolio equalling **320x** the original portfolio (compared to around 40x if we just simply hold the market index. Note that during this time, the crypto market exploded exponentially in size, hence resulting in this *seemingly crazy* returns).  

![alttext](https://github.com/dang-trung/crypto-sentiment-index/blob/master/output/01_figures/strat.svg)

## Table of Contents
- [Project Description](#project-description)
  - [Introduction](#introduction)
  - [Methods Used](#methods-used)
  - [Dependencies](#dependencies)
  - [Interesting Results to Keep You Reading](#interesting-results-to-keep-you-reading)
- [Table of Contents](#table-of-contents)
- [Getting Started](#getting-started)
  - [How to Run](#how-to-run)
  - [Project Structure](#project-structure)
  - [Dependent Variable](#dependent-variable)
  - [Sentiment Indicators](#sentiment-indicators)
- [Read More](#read-more)
## Getting Started

### How to Run
(`$` indicates these are terminal commands)
1. Clone this repo:
`$ git clone https://github.com/dang-trung/crypto-sentiment-index/`
2. Create your environment (virtualenv):  
`$ virtualenv -p python3 venv`  
`$ source venv/bin/activate` (bash) or `venv\Scripts\activate` (windows)   
`$ (venv) cd crypto-sentiment-index`  
`$ (venv) pip install -e`  

    Or (conda):  
`$ conda env create -f environment.yml`  
`$ conda activate crypto-sentiment-index`  
3. In terminal:  
`$ python -m crypto-sentiment-index`  

### Project Structure
```
├─ data                      
│  ├─ 00_external            <- Contain rules for sentiment analysis & text processing
│  ├─ 01_raw                 <- Immutable text messages retrieved from stockTwits/reddit
│  └─ 02_processed           <- Data used to developed models
│     ├─ direct              <- Direct sentiment indicators
│     ├─ indirect            <- Indirect sentiment indicators
│     ├─ crix.json           <- Target variable
│     └─ final_dataset.csv
├─ output                    <- Generated output
│  ├─ 01_figures             <- Figures
│  └─ 02_reports             <- Analysis reports
│     ├─ full_thesis.pdf     <- Final thesis
│     └─ report_chapters.pdf <- Analysis chapters (skip literature review etc.)
├─ src                       <- Source code
│  ├─ data                   <- Package of modules that retrieve raw data
│  │  ├─ __init__.py         
│  │  ├─ __main__.py         <- Run in terminal: $ python -m src.data
│  │  ├─ convert_ts.py       <- Functions to convert between different formats of time
│  │  ├─ others.py           <- Get messages from other sources (google volume, trading volume, FT articles)
│  │  ├─ reddit.py           <- Get messages from reddit
│  │  └─ stocktwits.py       <- Get messages from stockTwits
│  ├─ process                <- Modules used to retrieve data 
│  │  ├─ __init__.py
│  │  ├─ __main__.py         <- Run in terminal: $ python -m src.process
│  │  ├─ gather_data.py      <- Gather all processed data into data/02_processed
│  │  ├─ sentiment_score.py  <- Function to score sentiment 
│  │  └─ text_process.py     <- Function to process text data (only info relevant to sentiment analysis remains)
│  ├─ __init__.py
│  ├─ model.py               <- Train the model using processed data from data/02_processed 
│  └─ visualize.py           <- Generate figures
├─ .gitattributes            <- Avoid GitHub mis-recognize figures in html format as codes
├─ .gitignore                <- Avoids uploading large data, system files, etc.
├─ LICENSE.md
├─ README.md                 
├─ environment.yml           <- Share conda enviroment
├─ requirements.txt          <- To reproduce analysis enviroment using pip
└─ setup.py                  <- Make the project pip installable with `$ pip install -e`

```

### Dependent Variable
Cryptocurrency market returns (computed using the market index CRIX,
retrieved [here](http://data.thecrix.de/data/crix.json),
see more on how the index is created at [Trimborn & Härdle (2018)](https://doi.org/10.1016/j.jempfin.2018.08.004)
or [those authors' website](https://thecrix.de/).)

### Sentiment Indicators
* Sentiment score of Messages on StockTwits, Reddit Submissions, Reddit Comments
  * Computed using dictionary-based sentiment analysis, lexicon used: crypto-specific lexicon by [Chen et al (2019)](http://dx.doi.org/10.2139/ssrn.3398423),
  retrieved at the main author's [personal page](https://sites.google.com/site/professorcathychen/resume).
  * StockTwits messages are retrieved through [StockTwits Public API](https://api.stocktwits.com/developers),
    Reddit data are retrieved using [PushShift.io Reddit API](https://github.com/pushshift/api).
* Messages volume on StockTwits, Reddit Submissions, Reddit Comments.
* Market volatility index VCRIX (see how the index is created: [Kolesnikova (2018)](https://edoc.hu-berlin.de/bitstream/handle/18452/20056/master_kolesnikova_alisa.pdf?sequence=3&isAllowed=y), retrieved [here](http://data.thecrix.de/data/crix11.json).)
* Market trading volume (retrieved using [Nomics Public API](https://docs.nomics.com/))

The sentiment index is simply the **first principal component** of these 9 indicators.


## Read More
For better understanding of the project, kindly read:
* the [analysis chapters](https://github.com/dang-trung/crypto-sentiment-index/blob/master/output/02_reports/report_chapters.pdf).
* Or the [full thesis](https://github.com/dang-trung/crypto-sentiment-index/blob/master/output/02_reports/full_thesis.pdf). 

<!-- MARKDOWN LINKS & IMAGES -->
[github-shield]: https://img.shields.io/badge/-GitHub-black.svg?style=social&logo=github&colorB=555
[github-url]: https://github.com/dang-trung/
[license-shield]: https://img.shields.io/github/license/dang-trung/crypto-return-predictor.svg?style=social
[license-url]: https://github.com/dang-trung/crypto-return-predictor/blob/master/LICENSE.md
[linkedin-shield]: https://img.shields.io/badge/-LinkedIn-black.svg?style=social&logo=linkedin&colorB=555
[linkedin-url]: https://linkedin.com/in/dang-trung
