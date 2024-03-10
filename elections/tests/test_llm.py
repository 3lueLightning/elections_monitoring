import pytest

import pandas as pd

from openai import OpenAI

from elections.sentiment_analysis import SentimentAnalysis
from elections.prompts.templates import example_1, example_2, example_3
from elections.prompts.validation import val_1


#import ipdb; ipdb.set_trace()
# df.loc[0, "analysis"].sentiments
# df.loc[0, "analysis"].sentiments[1].citations


@pytest.fixture
def article_ex1():
    df = pd.DataFrame([
        {
            "article_id": 1,
            "title": example_1.TITLE,
            "description": example_1.DESCRIPTION,
            "text": example_1.TEXT,
        }
    ])
    return df


@pytest.fixture
def article_ex2():
    df = pd.DataFrame([
        {
            "article_id": 2,
            "title": example_2.TITLE,
            "description": example_2.DESCRIPTION,
            "text": example_2.TEXT,
        }
    ])
    return df


@pytest.fixture
def article_ex3():
    df = pd.DataFrame([
        {
            "article_id": 3,
            "title": example_3.TITLE,
            "description": example_3.DESCRIPTION,
            "text": example_3.TEXT,
        }
    ])
    return df


@pytest.fixture
def article_val1():
    df = pd.DataFrame([
        {
            "article_id": 4,
            "title": val_1.TITLE,
            "description": val_1.DESCRIPTION,
            "text": val_1.TEXT,
        }
    ])
    return df


@pytest.mark.openai
def test_openai_connection():
    """"
    Test that we can connect to OpenAI's API
    """
    client = OpenAI()
    sentiment = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": "Say this is a test"}],
    )

    resp = sentiment.choices[0].message.content
    assert resp == 'This is a test.', "OpenAI's API is not working"


@pytest.mark.openai
def test_prompt_example_1(article_ex1):
    sentiment_analysis = SentimentAnalysis()
    sentiment_analysis.articles_df = article_ex1
    df = sentiment_analysis.get_sentiments(save=False)
    
    assert len(df) == 1, "The dataframe should have only one row"
    
    sentiments = df.loc[0, "analysis"].sentiments
    names = [sent.name for sent in sentiments]
    assert set(names) == set(example_1.POLITICIANS), \
        "Politician names don't match, expecting: {example_1.POLITICIANS} "\
        "got: {names}"
    
    pns_sentiments = [sent for sent in sentiments if sent.name == "Pedro Nuno Santos"][0]
    montenegro_sentiments = [sent for sent in sentiments if sent.name == "Luís Montenegro"][0]
    rocha_sentiments = [sent for sent in sentiments if sent.name == "Rui Rocha"][0]
    
    assert pns_sentiments.score > 0.5, "Pedro Nuno Santos should have a score above 0.5"
    assert montenegro_sentiments.score < 0.6, "Luís Montenegro should have a score below 0.6"
    assert rocha_sentiments.score is None, "Rui Rocha should have a score of None"


@pytest.mark.openai
def test_prompt_example_2(article_ex2):
    sentiment_analysis = SentimentAnalysis()
    sentiment_analysis.articles_df = article_ex2
    df = sentiment_analysis.get_sentiments(save=False)
    
    assert len(df) == 1, "The dataframe should have only one row"
    
    sentiments = df.loc[0, "analysis"].sentiments
    names = [sent.name for sent in sentiments]

    # excluding Ventura from the analysis
    assert set(names) == set(example_2.POLITICIANS) or set(names) == {'Pedro Nuno Santos', 'Paulo Raimundo'}, \
        "Politician names don't match, expecting: {example_2.POLITICIANS} "\
        "got: {names}"
    
    pns_sentiments = [sent for sent in sentiments if sent.name == "Pedro Nuno Santos"][0]
    raimundo_sentiments = [sent for sent in sentiments if sent.name == "Paulo Raimundo"][0]
    
    assert pns_sentiments.score <= 0.55, "Pedro Nuno Santos should have a score above 0.5"
    assert raimundo_sentiments.score > .5, "Raimudo should have a score above 0.5"


@pytest.mark.openai
def test_prompt_example_3(article_ex3):
    sentiment_analysis = SentimentAnalysis()
    sentiment_analysis.articles_df = article_ex3
    df = sentiment_analysis.get_sentiments(save=False)
    
    assert len(df) == 1, "The dataframe should have only one row"
    
    sentiments = df.loc[0, "analysis"].sentiments
    names = [sent.name for sent in sentiments]
    
    assert set(names) == set(example_3.POLITICIANS), \
        "Politician names don't match, expecting: {example_3.POLITICIANS} "\
        "got: {names}"
    
    pns_sentiments = [sent for sent in sentiments if sent.name == "Pedro Nuno Santos"][0]
    other_scores = [sent.score for sent in sentiments if sent.name != "Pedro Nuno Santos"]
    
    assert pns_sentiments.score <= 0.45, "Pedro Nuno Santos should have a score above 0.45"
    assert not any(other_scores), "besides PNS no one should have scores"


def test_promt_val_1(article_val1):
    sentiment_analysis = SentimentAnalysis()
    sentiment_analysis.articles_df = article_val1
    df = sentiment_analysis.get_sentiments(save=False)
    print("here")
