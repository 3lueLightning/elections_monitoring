import pytest

import pandas as pd

from openai import OpenAI

from elections.sentiment_analysis import SentimentAnalysis
from elections.prompts.templates import example_1

@pytest.fixture
def article_1():
    df = pd.DataFrame([
        {
            "article_id": 1,
            "title": example_1.TITLE,
            "description": example_1.DESCRIPTION,
            "text": example_1.TEXT,
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
def test_prompt_example_1(article_1):
    sentiment_analysis = SentimentAnalysis()
    sentiment_analysis.articles_df = article_1
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
