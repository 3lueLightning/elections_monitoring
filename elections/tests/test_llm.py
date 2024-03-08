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
    import pdb; pdb.set_trace()
    pass