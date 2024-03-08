from typing import Optional

import sqlite3
import instructor
import pandas as pd

from tqdm import tqdm
from openai import OpenAI
from pydantic import ValidationError

from elections import constants
from elections.data_schemas import ArticleSentiment
from elections.scrapers.news_scraper import NewsScraper
from elections.prompts.templates import system_prompt
from elections.utils import (
    full_logger, safe_json_loads,  safe_model_validate_json, safe_model_dumps
)


# Currently replaced by printing because of a bug in my editor VScode
#logger = full_logger(constants.LOG_LVL, constants.SENTIMENT_LOG_FN, to_console=False)


class MaxRetriesExceeded(Exception):
    pass


class SentimentAnalysis:
    """
    This class is responsible for extracting the sentiment of articles from the database,
    using OpenAI's API.
    """
    def __init__(self):
        self.client = instructor.patch(OpenAI())
        self.articles_df = pd.DataFrame()
        self.sentiments = []
        self.articles_counter = 0
        print(f"using model: {constants.OPENAI_GPT_MODEL}")
        
    def load_articles(self, n_articles=None, refresh=False, query=None) -> None:
        """
        Loads the articles from the database that will be used to extrac sentiments.
        
        Args:
            n_articles: the number of articles to load (ignored if query is not None).
            refresh: whether to load all articles or just the ones that haven't been analyzed yet or
                that have not been sucessfully analyzed before (ignored if query is not None).
            query: a custom query to load the articles (overides all other arguments). It must return
                the following columns: article_id, title, description, text
        
        Returns:
            None. It set articles_df attribute to the loaded articles.
        """
        if query is not None:
            df = NewsScraper.load_articles(query)
            assert not df.empty, "No articles found"
            all_cols_in = pd.Series(["article_id", "title", "description", "text"]).isin(df.columns).all()
            assert all_cols_in, "all this columns should present in your query with the following names:\
                article_id, title, description, text"
            self.articles_df = df
            return
        if refresh:
            query = "SELECT article_id, title, description, text FROM articles"
        else:
            query = """
                SELECT 
                    atc.article_id, title, description, text
                FROM articles atc
                LEFT JOIN article_sentiments atc_s
                ON atc.article_id = atc_s.article_id
                WHERE atc_s.analysis IS NULL
            """
        if n_articles is not None:
            query = f"{query} LIMIT {n_articles}"
        self.articles_df = NewsScraper.load_articles(query)
    
    def filter_articles(self) -> None:
        """
        Many extracted articles are irrelavant to the election analysis depite having relevant search
        queries. To accommodated for that we filter the articles to only include those that mention
        politicians in the title or description or text.
        """
        assert not self.articles_df.empty, "No articles loaded"
        
        aliases = [alias for aliases in constants.POLITICIAN_ALIASES.values() for alias in aliases]
        names_n_aliases = aliases + constants.POLITICIANS
        mask_politician_in_title = (
            (self.articles_df["title"] + self.articles_df["description"] + self.articles_df["text"])
            .str.contains("|".join(names_n_aliases), case=False)
        )
        self.articles_df = self.articles_df[mask_politician_in_title]
    
    def get_article_sentiment(self, title: str, description: str, text: str) -> pd.DataFrame:
        """
        Receives the title, description and text of an article and identifies each politician present 
        in the article as well as his/her positivity score (0 very negative and 1 very positive). To
        prevent hallucinations, the model has to provide evidence for his score in the form citations
        from the article.
        
        Returns:
            a dataframe containing the following data (for more info read get_sentiments method):
                1. analysis containing a ArticleSentiment object.
                2. system_prompt: the system prompt used by the model to generate the response.
                3. user_prompt: the user prompt used by the model to generate the response.
                4. error_message: if the model fails to generate a response, the error message.
        """
        article_n_meta = title + "\n" + description + "\n" + text
        politicians_present = [
            politician for politician in constants.POLITICIANS if politician in article_n_meta
        ]
        politicians_present_str = ", ".join(politicians_present)
        system_prompt = system_prompt.SYSTEM_PROMPT
        user_prompt = system_prompt.USER_PROMPT.format(
            title=title, description=description, text=text, politicians=politicians_present_str
        )
        
        try:
            # to see the raw response: resp._raw_response.model_dump_json(indent=2)
            resp = self.client.chat.completions.create(
                model=constants.OPENAI_GPT_MODEL,
                response_model=ArticleSentiment,
                validation_context={
                    "article_n_meta": article_n_meta,
                    "politicians_present": politicians_present
                },
                max_retries=constants.MAX_RETRIES,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt},
                ],
            )
            val_error = None
        except (ValidationError, ValueError) as e:
            print(f"Model schema error:\n{e}")
            resp = None
            val_error = e.json()
            
        
        df = pd.DataFrame({
            "analysis": [resp],
            "system_prompt": [system_prompt],
            "user_prompt": [user_prompt],
            "error_message": [val_error],
        })
        return df
    
    def get_sentiments(
            self,
            freq: int=5,
            save: bool=True,
            max_failures: int=None) -> Optional[pd.DataFrame]:
        """
        After the articles are loaded, this method iterates over each article and extracts the
        sentiement of each one. It returns either a pandas dataframe with the sentiments or 
        save the dataframe to the database.
        
        Args:
            freq: the frequency of the logging
            save: whether to save the sentiments in the database
            max_failures: the maximum number of failures to extract a article sentiments tolerated
        
        Returns: 
            the following data in dataframe or in sql table:
                1. analysis containing a ArticleSentiment object, type of list contianing each 
                    politician mentioned in the article, along with his/her positivity score (0 
                    very negative and 1 very positive) and citations to back it up. The list of
                    citations includes the acutal quote and a positivity score for the quote as 
                    well as the author if possible. If all citations regarding a politician are
                    factual is overall score will be None and the citations will be empty. This
                    field will be None if the model fails to generate a response.
                2. system_prompt: the system prompt used by the model to generate the response.
                3. user_prompt: the user prompt used by the model to generate the response.
                4. error_message: if the model fails to generate a response, the error message.
        
        Raises:
            MaxRetriesExceeded: read max_failures argument
        """
        assert not self.articles_df.empty, "No articles loaded"
        N = len(self.articles_df)
        
        if save:
            engine = sqlite3.connect(constants.NEWS_DB)
        
        self.sentiments = []
        self.articles_counter = 0
        for i, row in tqdm(self.articles_df.reset_index().iterrows(), total=N):
            #if i % freq == 0:
                #logger.info(f"Processing article {i + 1} of {N}")
                #print(f"Processing article {i + 1} of {N}")
            sentiment = self.get_article_sentiment(row["title"], row["description"], row["text"])
            sentiment.insert(loc=0, column="article_id", value=row["article_id"])
            if not sentiment.empty:
                self.sentiments.append(sentiment)
                self.articles_counter += 1
                if self.articles_counter % freq == 0 or i == N - 1:
                    if save:
                        self._save_sentiments(engine)
                    else:
                        #logger.info(f"Extracted {self.articles_counter} of {N}")
                        print(f"Extracted {self.articles_counter} of {N}")
            if max_failures is not None and i + 1 - self.articles_counter >= max_failures:
                raise MaxRetriesExceeded(f"Failed to extract {max_failures} articles")
        if save:
            engine.close()
            return None
        
        return pd.concat(self.sentiments, ignore_index=True)

    def _save_sentiments(self, engine) -> None:
        sentiments_df = pd.concat(self.sentiments)
        sentiments_df["analysis"] = sentiments_df["analysis"].apply(safe_model_dumps)
        sentiments_df.to_sql("article_sentiments", con=engine, if_exists="append", index=False)
        self.sentiments = []
        #logger.info(f"Saved in DB {self.articles_counter} of {N}")
        print(f"Saved in DB {self.articles_counter} of {len(self.articles_df)}")
    
    @staticmethod
    def load_article_sentiments(query: str="SELECT * FROM article_sentiments") -> pd.DataFrame:
        with sqlite3.connect(constants.NEWS_DB) as engine:
            df = pd.read_sql(query, con=engine)
        if "analysis" in df.columns:
            df["analysis"] = df["analysis"].apply(safe_model_validate_json, model=ArticleSentiment)
        if "error_message" in df.columns:
            df["error_message"] = df["error_message"].apply(safe_json_loads)
        return df
