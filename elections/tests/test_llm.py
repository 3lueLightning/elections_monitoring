import pytest

from openai import OpenAI


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
