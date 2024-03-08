from typing import Optional
from datetime import date

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import sqlite3

from elections import constants
from elections.scrapers.news_scraper import NewsScraper
from elections.data_schemas import ArticleSentiment
from elections.sentiment_analysis import SentimentAnalysis
from elections.utils import safe_model_validate_json, safe_json_loads, full_logger


logger = full_logger(constants.LOG_LVL, constants.SENTIMENT_LOG_FN, to_console=False)


def _map_alises_to_name(df: pd.DataFrame) -> pd.DataFrame:
    df_ = df.copy()
    alias_to_name = {alias: politician for politician, aliases 
        in constants.POLITICIAN_ALIASES.items() for alias in aliases
    }
    df_["name"] = df_["name"].replace(alias_to_name)
    return df_

    
def load_sentiments() -> pd.DataFrame:
    """
    Load the sentiments from the database and return a DataFrame with the results.
    """
    query = """
        WITH latest_sentiments AS (
            SELECT 
                RANK() OVER (PARTITION BY article_id ORDER BY sentiment_id DESC) recency,
                *
            FROM article_sentiments
            WHERE 
                analysis IS NOT NULL
        )
        SELECT
            ls.article_id,
            ls.analysis,
            atc.title,
            atc.description,
            atc.text,
            atc.pubdate,
            atc.publisher
        FROM latest_sentiments ls
        INNER JOIN articles atc
            ON ls.article_id = atc.article_id  
        WHERE recency = 1
    """
    with sqlite3.connect(constants.NEWS_DB) as conn:
        df = pd.read_sql(query, conn)
    
    # data processing
    df["pubdate"] = pd.to_datetime(df["pubdate"])
    df["analysis"] = df["analysis"].apply(
        safe_model_validate_json, model=ArticleSentiment
    )
    
    # validations
    duplicated_ids = df["article_id"].duplicated()
    assert not duplicated_ids.any(), \
        f"There are {duplicated_ids.sum()} duplicate article_id in the database"
    
    logger.info(f"Loaded {len(df)} sentiments from the database.")
    return df


def load_errors(counts_only=False) -> Optional[pd.DataFrame]:
    """
    Load the errors from the database and return a DataFrame with the results.
    """
    if counts_only:
        error_processing_query = "COUNT(1)"
    else:
        error_processing_query = """
            article_id,
            system_prompt,
            user_prompt,
            error_message
        """
        
    query = f"""
        WITH latest_sentiments AS (
            SELECT 
                RANK() OVER (PARTITION BY article_id ORDER BY sentiment_id DESC) recency,
                *
            FROM article_sentiments
            WHERE 
                analysis IS NULL
        )
        SELECT
            {error_processing_query} n
        FROM latest_sentiments
    """
    
    with sqlite3.connect(constants.NEWS_DB) as conn:
        df = pd.read_sql(query, conn)
    
    if counts_only:
        logger.info(f"There are {df.loc[0, "n"]} errors in the last sentiment " +
            "analysis run of all articles")
        return
    
    df["error_message"] = df["error_message"].apply(safe_json_loads)
    
    logger.info(f"Loaded {len(df)} errors from the database.")
    return df


def plot_publishers(df) -> None:
    df["publisher"].value_counts().plot.bar()
    plt.xticks(rotation=60, ha='right')


def _expand_analysis_col(row: pd.Series) -> pd.DataFrame:
    analysis = []
    sentiments = row["analysis"].sentiments
    if not sentiments:
        df = pd.DataFrame([
            {
                "quote": None,
                "score": None,
                "name": None,
                "article_id": row["article_id"]
            }
        ])
        return df
    for sent in sentiments:
        if sent.citations:
            df = pd.DataFrame(
                [{"quote": cite.quote, "quote_score": cite.score, 
                  "author": cite.author} for cite in sent.citations]
            )
        else:
            df = pd.DataFrame([{"quote": None, "score": None}])
        df["name"] = sent.name
        df["score"] = sent.score
        df["article_id"] = row["article_id"]
        analysis.append(df)
    
    analysis = [df.dropna(axis=1, how='all') for df in analysis]
    return pd.concat(analysis, ignore_index=True)


def expand_sentiments(df: pd.DataFrame) -> pd.DataFrame:
    """
    Expand the sentiments DataFrame by creating a row for each citation in 
    the analysis column.
    """
    expanded = df[["article_id", "analysis"]].apply(_expand_analysis_col, axis=1)
    expanded_df = pd.concat(
        [df.dropna(axis=1, how='all') for df in expanded]
        , ignore_index=True
    )
    expanded_df = _map_alises_to_name(expanded_df)
    
    # filter out the names that don't belong to current party leaders
    mask_politican = expanded_df["name"].isin(constants.POLITICIANS)
    return expanded_df[mask_politican]


def get_article_score_stats(df):
    mask_has_score = ~df["score"].isnull()
    ids_with_score = df.loc[mask_has_score, "article_id"].unique()
    ids_no_score_set = set(df["article_id"].unique()) - set(ids_with_score)
    ids_no_score = np.sort(list(ids_no_score_set))
    summary_df = pd.DataFrame({
        "n": [len(ids_with_score), len(ids_no_score)]
    }, index=["articles_with_score", "articles_without_score"])
    return summary_df


def plot_politician_article_refs(df) -> None:
    with sns.axes_style("whitegrid"):
        sns.barplot(df["name"].value_counts(), orient = 'h')
        plt.xlabel("Number of articles")
        plt.ylabel("")

