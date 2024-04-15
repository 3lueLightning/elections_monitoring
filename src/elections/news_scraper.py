import json

from copy import deepcopy
from datetime import datetime
from typing import Optional

import sqlite3
import pandas as pd
import matplotlib.pyplot as plt

from gnews import GNews
from unidecode import unidecode
from newspaper import Article, ArticleException

from elections import constants
from elections.utils import full_logger, safe_json_dumps


logger = full_logger(constants.LOG_LVL, constants.SCRAPE_LOG_FN)


class NewsScraper():
    """
    The articles scrapping operates in two steps:
    1. Get the metadata from the articles (via GNews API): get_metadata()
    2. Get the actually content from the articles (via newspaper3k API): get_article()
    """
    # names returned by GNews
    table_name = "articles"
    url_name = "url"
    title_name = "title"
    description_name = "description"
    pubdate_name = "published date"
    pubdate_format = "%a, %d %b %Y %H:%M:%S %Z"
    publisher_name = "publisher"
    news_outlet_name = "title"
    
    def __init__(self, query: str, start_date: datetime, end_date: datetime) -> None:
        self.query = query
        self.start_date = start_date
        self.end_date = end_date
        self.max_results = None
        self.query_metadata = []
        self.news = pd.DataFrame()

    @staticmethod
    def _format_metadata(metadata: list[dict]) -> list[dict]:
        formated_metadata = []
        urls = NewsScraper.load_past_urls()
        
        for raw_article_metadata in metadata:
            article_metadata = {}
            article_metadata["title"] = raw_article_metadata.get(NewsScraper.title_name)
            article_metadata["description"] = raw_article_metadata.get(NewsScraper.description_name)
            try:
                article_metadata["pubdate"] = datetime.strptime(
                    raw_article_metadata[NewsScraper.pubdate_name],
                    NewsScraper.pubdate_format
                )
            except KeyError:
                article_metadata["pubdate"] = None
            publisher_info = raw_article_metadata.get(NewsScraper.publisher_name)
            article_metadata["publisher"] = publisher_info.get(NewsScraper.news_outlet_name)
            article_metadata["url"] = raw_article_metadata.get(NewsScraper.url_name)
            if article_metadata["url"] is not None and article_metadata["url"] not in urls:
                formated_metadata.append(article_metadata)
                urls.add(article_metadata["url"])
            
        return formated_metadata
            
    def get_metadata(self, max_results: Optional[int]=None) -> None:
        logger.info(f"Getting metadata for {self.query}")
        google_news = GNews(
            language=constants.LANGUAGE,
            country=constants.COUNTRY,
            start_date=self.start_date,
            end_date=self.end_date,
            max_results=max_results,
        )
        query_metadata = google_news.get_news(self.query)
        self.query_metadata = NewsScraper._format_metadata(query_metadata)
        logger.info(f"Found {len(self.query_metadata)} metadata entries")
    
    @staticmethod
    def _extract_content(article: Article, metadata: dict) -> dict:
        news = deepcopy(metadata)
        article.nlp()
        news["summary"] = article.summary
        news["keywords"] = article.keywords
        news["text"] = article.text
        return news
        
    def get_article(self) -> None:
        if not self.query_metadata:
            logger.info("No metadata to get articles from")
            return
        logger.info(f"Getting articles")
        
        news = []
        for article_metadata in self.query_metadata:
            article = Article(url=article_metadata["url"], language=constants.LANGUAGE)
            article.download()
            try:
                article.parse()
            except ArticleException:
                continue
            news.append(self._extract_content(article, article_metadata))
        self.news = pd.DataFrame(news)
        logger.info(f"Found {len(self.news)} articles")
    
    def save_articles(self) -> None:
        if self.news.empty:
            logger.info("No articles to save")
            return
        news = self.news.copy()
        news["keywords"] = news["keywords"].apply(safe_json_dumps, ensure_ascii=False)
        news["creation_datetime"] = datetime.now()
        news["query"] = self.query
        with sqlite3.connect(constants.NEWS_DB) as engine:
            news.to_sql("articles", con=engine, if_exists="append", index=False)
        logger.info(f"Saved {len(news)} articles")
    
    @staticmethod
    def load_articles(query: str="SELECT * FROM articles") -> pd.DataFrame:
        with sqlite3.connect(constants.NEWS_DB) as engine:
            news = pd.read_sql(query, con=engine)
        if "keywords" in news:
            news["keywords"] = news["keywords"].apply(json.loads)
        if "pubdate" in news:
            news["pubdate"] = pd.to_datetime(news["pubdate"])
        return news
    
    @staticmethod
    def load_past_urls() -> set:
        query = f"SELECT url FROM {NewsScraper.table_name}"
        try:
            with sqlite3.connect(constants.NEWS_DB) as engine:
                urls = pd.read_sql(query, con=engine)
        except pd.errors.DatabaseError:
            return set()
        return set(urls["url"])
    
    @staticmethod
    def count_daily_politician_references() -> pd.DataFrame:
        """
        Count the number of references to each politician per day
        """
        
        case_when_list = []
        as_politician_col_list = []
        for politician in constants.POLITICIANS:
            politician = politician.lower()
            sanitised_name = unidecode(politician) # remove accents
            has_politician_col = "has_" + sanitised_name.replace(' ', '_')
            case_when = f"CASE WHEN INSTR(LOWER(title || text), '{politician}') \
                THEN 1 ELSE 0 END AS {has_politician_col}"
            case_when_list.append(case_when)
            as_politician_col_list.append(has_politician_col)
        
        sum_cols = [
            f"SUM({col}) {col.replace("has", "n")}" for col in as_politician_col_list
        ]
        
        query = f"""
        WITH politicians_referred AS (
            SELECT
                DATE(pubdate) pubday,
                {",\n\t".join(case_when_list)}
            FROM articles
        )
        SELECT
            \tpubday,
            \t{",\n\t".join(sum_cols)}
        FROM politicians_referred
        GROUP BY pubday
        ORDER BY pubday
        """
        
        with sqlite3.connect(constants.NEWS_DB) as engine:
            daily_ref_counts = pd.read_sql(query, con=engine)
        return daily_ref_counts
    
    @staticmethod
    def plot_daily_politician_ref_counts() -> None:
        df = NewsScraper.count_daily_politician_references()
        all_cols = [col for col in df.columns if col.startswith("n_")]
        n = len(all_cols)
        
        print(df[all_cols].sum())
        
        y_max = df[all_cols].max().max()
        fig, axes = plt.subplots(n, 1, figsize=(15, 6 * n))
        plt.subplots_adjust(hspace=0.3)
        for col, ax in zip(all_cols, axes):
            df.plot(x="pubday", y=col, kind="line", ax=ax)
            ax.set_title(col.replace("n_", "").replace("_", " "))
            ax.set_ylabel("number of articles")
            ax.set_xlabel("publishing date")
            ax.set_ylim(0, y_max + 1)
        plt.show()
    
    @staticmethod
    def count_daily_articles() -> pd.DataFrame:
        query = """
        SELECT
            DATE(pubdate) pubday,
            COUNT(*) n_articles
        FROM articles
        GROUP BY pubday
        """
        with sqlite3.connect(constants.NEWS_DB) as engine:
            daily_article_counts = pd.read_sql(query, con=engine)
        return daily_article_counts
    
    def plot_daily_article_counts() -> None:
        df = NewsScraper.count_daily_articles()
        fig, ax = plt.subplots(1, 1, figsize=(15, 8))
        df.plot(x="pubday", y="n_articles", kind="line", ax=ax)
        ax.set_title("Number of articles per day")
        ax.set_ylabel("number of articles")
        ax.set_xlabel("publishing date")
        ax.set_ylim(0, None)
        plt.show()
    