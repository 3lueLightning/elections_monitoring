import json

from copy import deepcopy
from datetime import datetime
from typing import Optional

import sqlite3
import pandas as pd

from gnews import GNews
from newspaper import Article, ArticleException

from elections import constants


class NewsScraper():
    # names returned by GNews
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
        self.query_metadata = [{}]
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
        google_news = GNews(
            language=constants.LANGUAGE,
            country=constants.COUNTRY,
            start_date=self.start_date,
            end_date=self.end_date,
            max_results=max_results,
        )
        query_metadata = google_news.get_news(self.query)
        self.query_metadata = NewsScraper._format_metadata(query_metadata)
    
    @staticmethod
    def _extract_content(article: Article, metadata: dict) -> dict:
        news = deepcopy(metadata)
        article.nlp()
        news["summary"] = article.summary
        news["keywords"] = article.keywords
        news["text"] = article.text
        return news

    #def validate_metadata(self) -> None:
    #   pass
        
    def get_article(self) -> None:
        assert self.query_metadata != [{}], "run get_metadata first"
        
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
    
    def save_articles(self) -> None:
        engine = sqlite3.connect(constants.NEWS_DB)
        news = self.news.copy()
        news["keywords"] = news["keywords"].apply(json.dumps, ensure_ascii=False)
        news["creation_datetime"] = datetime.now()
        news["query"] = self.query
        news.to_sql("articles", con=engine, if_exists="append", index=False)
    
    @staticmethod
    def load_articles(query: str="SELECT * FROM articles") -> pd.DataFrame:
        engine = sqlite3.connect(constants.NEWS_DB)
        news = pd.read_sql(query, con=engine)
        if "keywords" in news:
            news["keywords"] = news["keywords"].apply(json.loads)
        return news
    
    @staticmethod
    def load_past_urls() -> set:
        engine = sqlite3.connect(constants.NEWS_DB)
        query = "SELECT url FROM articles"
        try:
            urls = pd.read_sql(query, con=engine)
        except pd.errors.DatabaseError:
            return set()
        return set(urls["url"])
    