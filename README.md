# Portuguese elections 2024
## Project intro
<p align="center">
  <img src="images/portugal_votes.jpg" alt="portugal votes" width="600"/>
</p>


This non-partisan project aims to analyse the media coverage of the various political parties participating in the the 2024 Portuguese Parlamentary elections. It then proceeds to analyse each news article's sentiment towards each candidate which hopefully can serve as proxy for overall sentiment towards that party.

Since portuguese politics focuses far more on the representatives of each party rather then the party itself each candidate will be the central point of this analysis. In addition, we will limit ourselves to the candidats of parties with parlamentary seat.

<p align="center">
  <img src="images/political_candidates.jpg" alt="portugal votes" width="600"/>
</p>

## Project structure
It consists of 3 parts, with the first 2 being ready and the 3rd under construction:
1.	**Collecting news articles**: 
    1. Collect articles on all the main candidates via a web-scraping API
    2. *Entry point*: `elections/main/1_articles_scraping.ipynb`
2.	**Sentiment analysis**:
    1.	Using the Open API with GPT-3.5 and GPT-4 to analyze the sentiment of each article and extract its content in a pydantic data structure, which can be validated and JSON serialized. 
    2.	Control for hallucinations automatically and allow for human validation.
    3.  *Entry point*: `elections/main/2_sentiment_analysis.ipynb`
3.	**Presenting the results**:
    1.	Create analysis and charts.
    2.	Create a streamlit site.
    3.  *Entry point*: under construction

Note: this is a one-off project therefore I didn’t go through the steps to productionize it.


## Next steps:
1. extract more articles:
    1. run extractor again, since the last extraction date time was on: 2024-03-05
    2. get more news outlets: some outlet are over represented (eg: SIC, Expressso), hence running searches specifying the outlet name could help get different ones
2. validate sentiment analysis:
    1. situation: currently out of the 686 articles scraped for 80 sentiment analysis didn't run successfully and 289 has no sentiment expressed
    2. possibilities:
        1. in the case of the numerous articles without sentiment some genuinely have no sentiment other might - investigation on-going
        2. the errors are due to validation error of the pydantic data model passed to instructor - understand how modify prompt to reduce errors. As a backup use GPT-4-turbo for some articles rather then GPT-3.5-turbo
3. create a **daily_mentions** SQLite table:
    1. mention_id: primary key
    2. politician_name
    3. date (which corresponds to articles pubdate)
    3. score: the average score of that politician
    4. n_articles: number of articles mentioning him/her
    5. n_pos_quotes: how many positive quotes
    6. n_neg_quotes: how many negative quotes
    7. NB: politician_name and date also form composite keys


