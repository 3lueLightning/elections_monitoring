from typing import Optional
from datetime import date, datetime, timedelta

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import sqlite3

from elections import constants
from elections.data_schemas import ArticleSentiment
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
        WITH sucessful_sentiments AS (
            SELECT 
                *
            FROM article_sentiments
            WHERE 
                analysis IS NOT NULL
        ),
        latest_sentiments AS (
            SELECT 
                RANK() OVER (PARTITION BY article_id ORDER BY sentiment_id DESC) recency,
                *
            FROM sucessful_sentiments
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
        with latest_sentiments AS (
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
        WHERE recency = 1
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


def plot_articles_by_publishers(df, top_n:int) -> None:
    with sns.axes_style("whitegrid"):
        df["publisher"].value_counts(ascending=False)[:top_n].plot.bar(color="#edd609")
        plt.xlabel("20 fontes principais")
        plt.ylabel("Numero de artigos")
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


def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    def _remove_empty_duplicates(df):
        not_null = ~df["quote"].isnull()
        if not_null.any():
            return df[not_null]
        return df.drop_duplicates(subset=["name"], keep="first")

    df_clean = (
        df
        .groupby(["article_id", "name"])
        .apply(_remove_empty_duplicates)
        .reset_index(drop=True)
    )
    return df_clean


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
    politician_refs = df.groupby("name")["article_id"].nunique().sort_values(ascending=False)
    print(
        politician_refs / politician_refs.sum()
    )
    colors = [
        constants.POLITICIAN_COLORS[name] for name in politician_refs.index
    ]
    with sns.axes_style("whitegrid"):
        ax = sns.barplot(
            politician_refs, 
            orient = 'h',
        )
        plt.xlabel("Numero de artigos referenciados")
        plt.ylabel("")
        for i, bar in enumerate(ax.patches):
            bar.set_color(colors[i])
        plt.show()


def plot_politician_daily_article_refs(df):
    start_date = datetime(2024, 2, 8)
    end_date = datetime(2024, 3, 9)

    mask = (df["pubdate"] >= start_date) & (df["pubdate"] <= end_date)
    df_ = df[mask].copy()
    df_["pubday"] = df_["pubdate"].dt.date
    daily_refs = (
        df_
        .groupby(["pubday", "name"])["article_id"]
        .nunique()
        .rename("n")
        .reset_index()
    )

    total_refs = daily_refs.groupby("name")["n"].sum().sort_values(ascending=False)
    colors = [
        constants.POLITICIAN_COLORS[name] for name in total_refs.index
    ]

    with sns.axes_style("whitegrid"):
        fig = plt.figure(figsize=(10, 6))
        ax = sns.lineplot(
            data=daily_refs,
            x="pubday",
            y="n",
            hue="name",
            hue_order=total_refs.index,
            palette=sns.color_palette(colors),
        )
        x_ticks = pd.date_range(
            start=start_date + timedelta(1),
            end=end_date,
            freq='7D'
        )
        plt.xticks(x_ticks, rotation=60, ha='right')
        plt.xlabel("data de publicação")
        plt.ylabel("Numero de artigos referenciados")
        # mark specific event
        # Plot a circle around specific graph value
        event_date = date(2024, 2, 28)
        event_val = 222
        ax.plot_date(event_date, event_val,
                        'og', # marker style 'o', color 'g'
                        fillstyle='none', # circle is not filled (with color)
                        ms=20.0) # size of marker/circle
        plt.text(
            event_date + timedelta(3),
            event_val,
            "Montengro atingido\ncom tinta verde",
            fontsize=12,
            ha='center'
        )
        plt.show()


def get_avg_politician_scores(df: pd.DataFrame) -> pd.DataFrame:
    assert "name" in df.columns, "first you must expand the sentiments"
    avg_scores = df.groupby("name")["score"].mean()
    avg_scores.sort_values(ascending=False, inplace=True)
    return avg_scores


def plot_politician_avg_scores(df: pd.DataFrame) -> None:
    """
    Plot the average scores for each politician.
    
    Args:
        df: A dataframe with expanded sentiments (ArticleSentiments convertes 
            into multiples rows, one for each quote in the article and a "name"
            column)
    
    Returns:
        a plot
    """
    avg_scores = get_avg_politician_scores(df)
    print(avg_scores)
    
    colors = [
        constants.POLITICIAN_COLORS[name] for name in avg_scores.index
    ]
    with sns.axes_style("whitegrid"):
        ax = sns.barplot(
            avg_scores, 
            orient = 'h',
        )
        plt.xlabel("Índice de positividade médio, sendo 0 muito negativo, 1 muito positivo")
        plt.ylabel("")
        for i, bar in enumerate(ax.patches):
            bar.set_color(colors[i])
        plt.show()


def plot_politicians_ridge(df: pd.DataFrame) -> None:
    """
    Generates a Ridge plot, which is an overlapping density plot for each politician
    
    Args:
        df: A dataframe with expanded sentiments (ArticleSentiments convertes 
            into multiples rows, one for each quote in the article and a "name"
            column)
    
    Returns:
        a plot
    """
    def label(label):
        ax = plt.gca()
        ax.text(
            0, .4, label, color='black', fontsize=13,
            ha="left", va="center", transform=ax.transAxes
        )
    
    def mean_plot(**kwargs):
        """
        Adds a vertical line at the mean of the data
        """
        data = kwargs.pop("data")
        x_col = kwargs.pop("x")
        ymin = kwargs.pop("ymin")
        ymax = kwargs.pop("ymax")
        return plt.vlines(data[x_col].mean(), ymin=ymin, ymax=ymax, **kwargs)

    # determine the order of density plots (the lowest average score on top of 
    # the graph and the highest at the bottom). Orders the colors accordingly
    # to have the party color match each politician
    avg_scores = get_avg_politician_scores(df)
    row_order = avg_scores.reset_index()["name"].tolist()[::-1]
    colors = [constants.POLITICIAN_COLORS[name] for name in row_order]
    palette = sns.set_palette(sns.color_palette(colors))

    with sns.axes_style("white", rc={"axes.facecolor": (0, 0, 0, 0), 'axes.linewidth':2}):
        g = sns.FacetGrid(
            df[~df.score.isnull()], 
            palette=palette, row="name", hue="name",
            hue_order=row_order, row_order=row_order, aspect=9, height=1.2
        )

        g.map_dataframe(sns.kdeplot, x="score", color='black', cut=0)
        g.map_dataframe(sns.kdeplot, x="score", fill=True, alpha=1, cut=0)
        g.map_dataframe(mean_plot, x="score", ymin=0, ymax=1.7, linewidth=2, color="yellow", linestyle="--")

        g.map(label, "score")
        g.figure.subplots_adjust(hspace=-0.5)
        g.set_titles("")
        g.set(yticks=[], xlabel="ìndice de postividade (0 muito negativo, 1 muito positivo)", ylabel="")
        g.despine( left=True)
        plt.suptitle('Distribuição de índice de positividade nos media', y=0.95)
