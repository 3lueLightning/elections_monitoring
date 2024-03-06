# Portuguese elections 2024

<p align="center">
  <img src="images/portugal_votes.jpg" alt="portugal votes"/>
</p>


This non-partisan project aims to analyse the media coverage of the various political parties with parlamentary seat that participate in the the 2024 Portuguese Parlamentary elections. It then proceeds to analyse the political commentators sentiement towards each candidate.  

. It consists of 3 parts, with the first 2 being ready:
1.	Collecting news articles: on all the main candidates via a web-scraping API.
2.	Sentiment analysis: 
    1.	using the Open API with GPT-3.5 and GPT-4 to analyze the sentiment of each article and extract its content in a pydantic data structure, which can be validated and JSON serialized. 
    2.	Control for hallucinations automatically and allow for human validation.
3.	Presenting the results:
    1.	Create analysis and charts.
    2.	Create a streamlit site.

Note: this is a one-off project therefore I didn’t go through the steps to productionize it.


## Current package is capable of:
1. extracting all news that match a given query and store it in a sqlite db
2. extract information from the various political parties (currently only PSD is implemented)
3. perform sentiment analysis via de OpenAI API
4. obtain a correctly formated pydantic object from OpenAI with a well defined schema

## Just done:
1. currently the **articles** SQLite table is created on the fly by pandas create a schema for it:  
    1. have all existing columns: title	description	pubdate	publisher	url	summary	keywords	text	creation_datetime	query
    2. add a primary key (**article_id**) column that must have an automatique increment
2. create system to fetch all information about all candidats (in constants.POLITICIANS) during a certain time period
    1. produce the necessary logs
    2. ensure that no article is extracted twice
    3. the system looks at the current date as the last extraction date and takes the max(creatation_datetime) in the articles table -1 day as the new extraction start date 
    4. NB: currently it will have manual trigger from a notebook or python file
3. created a **article_sentiment** SQLite table with the sentiment analysis of each article:
    1. article_id
    2. analysis (extracted from OpenAI)
    3. system_prompt
    4. user_prompt

## Next steps:
All the above was just performed with a few use cases, now I have to scale it:  
1. currently there are 686 articles scrapped, should attempt to get more.
    1. maybe the scrapping order as an effect on the number of results obtained by each politician, so I should randomise it.
2. add validation to the data obtained from the OpenAI API, correct errors:
    1. sometimes it identifies politicians that are no in the text
    2. it fails to find citations for politicians that are present
3. create a **daily_mentions** SQLite table:
    1. mention_id: primary key
    2. politician_name
    3. date (which corresponds to articles pubdate)
    3. score: the average score of that politician
    4. n_articles: number of articles mentioning him/her
    5. n_pos_quotes: how many positive quotes
    6. n_neg_quotes: how many negative quotes
    7. NB: politician_name and date also form composite keys


