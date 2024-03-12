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

## Results
The results of this project are presented in [this LinkedIn article](https://www.linkedin.com/pulse/intelig%252525C3%252525AAncia-artificial-desvenda-disparidades-na-das-elei%252525C3%252525A7%252525C3%252525B5es-diogo-paxse/), in Portuguese.
English version coming soon.

## Project structure
It consists of 3 parts, with the first 2 being ready and the 3rd under construction:
1.	**Collecting news articles**: 
    1. Collect articles on all the main candidates via a web-scraping API
    2. *Entry point*: `src/elections/main/1_articles_scraping.ipynb`
2.	**Sentiment analysis**:
    1.	Using the Open API with GPT-3.5 and GPT-4 to analyze the sentiment of each article and extract its content in a pydantic data structure, which can be validated and JSON serialized. 
    2.	Control for hallucinations automatically and allow for human validation.
    3.  *Entry point*: `src/elections/main/2_sentiment_analysis.ipynb`
3.	**Presenting the results**:
    1.	Create analysis and charts:
        1. can show overall sentiment of politicican
        2. ridge plot (kind of kernel density estimate) of the scores of each quote associated to a politician
        3. show the evolution of the politicians score
        4. show media coverage of each politician
    3.  *Entry point*: `src/elections/main/1_sentiment_analysis.ipynb`

Note: this is a one-off project therefore I didn’t go through the steps to productionize it.
