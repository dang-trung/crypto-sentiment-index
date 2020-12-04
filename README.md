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
    Generation & Return Predictability.
  </p>

## Project Description
### Introduction

* **Objective**: Master's Degree Graduation Thesis.

* **Abstract**:

* **Status**: [Active, On-Hold, Completed]

### Methods Used
* Method 1
* Method 2
* Method 3

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



### Cool Results

## Table of Contents
https://luciopaiva.com/markdown-toc/

## Getting Started

### How to Run
(`$` indicates these are terminal commands)
1. Clone this repo:
`$ git clone [repo-link]`
2. Create your environment (virtualenv):  
`$ virtualenv -p python3 venv`  
`$ source venv/bin/activate` (bash) or `venv\Scripts\activate` (windows)   
`$ (venv) cd [repo-name]`  
`$ (venv) pip install -e`  

    Or (conda):  
`$ conda env create -f environment.yml`  
`$ conda activate [repo-name]`  
3. In terminal:  
`$ python -m [repo-name]`  

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

### Data Storage
1.  
2.  
3.

## Results

## Read More
For better understanding of the project, kindly read the [report]([link-to-report]).

<!-- MARKDOWN LINKS & IMAGES -->
[github-shield]: https://img.shields.io/badge/-GitHub-black.svg?style=social&logo=github&colorB=555
[github-url]: https://github.com/dang-trung/
[license-shield]: https://img.shields.io/github/license/dang-trung/crypto-return-predictor.svg?style=social
[license-url]: https://github.com/dang-trung/crypto-return-predictor/blob/master/LICENSE.md
[linkedin-shield]: https://img.shields.io/badge/-LinkedIn-black.svg?style=social&logo=linkedin&colorB=555
[linkedin-url]: https://linkedin.com/in/dang-trung
