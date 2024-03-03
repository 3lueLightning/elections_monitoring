import json
import pytest

from pydantic import ValidationError

from elections.data_schemas import Citation, Sentiment


@pytest.fixture
def correct_citation():
    citation = {
        "quote": "some slightly negative quote", 
        "score": 0.4
    }
    return citation


@pytest.fixture
def broken_citation():
    citation = {
        "quote": "", 
        "score": 1.4
    }
    return citation


@pytest.fixture
def correct_sentiment_with_score(correct_citation):
    sentiment = {
        "name": "Politician A", 
        "score": 0.4, 
        "citations":[correct_citation]
    }
    return sentiment


@pytest.fixture
def correct_sentiment_without_score():
    sentiment = {
        "name": "Politician B", 
        "score": None, 
        "citations":[]
    }
    return sentiment


@pytest.fixture
def broken_sentiment_score_without_citations():
    sentiment = {
        "name": "Politician C", 
        "score": .6, 
        "citations":[]
    }
    return sentiment


@pytest.fixture
def broken_sentiment_citations_without_score(correct_citation):
    sentiment = {
        "name": "Politician D", 
        "score": None, 
        "citations":[correct_citation]
    }
    return sentiment    


def test_correct_citation(correct_citation):
    citation = Citation(**correct_citation)
    assert citation.quote == "some slightly negative quote"
    assert citation.score == 0.4


def test_broken_citation(broken_citation):
    with pytest.raises(ValidationError) as val_error:
        Citation(**broken_citation)
    
    (quote_error, proba_error) = val_error.value.errors()
    assert quote_error["type"] == 'string_too_short', "quote must have multiple characters"
    assert proba_error["type"] == 'less_than_equal', "score must be between 0 and 1"


def test_correct_sentiment_with_score(correct_sentiment_with_score, correct_citation):
    sentiment = Sentiment(**correct_sentiment_with_score)
    sentiment.name == "Politician A"
    sentiment.score == 0.4
    sentiment.citations == [correct_citation]


def test_correct_sentiment_without_score(correct_sentiment_without_score):
    sentiment = Sentiment(**correct_sentiment_without_score)
    sentiment.name == "Politician B"
    sentiment.score == None
    sentiment.citations == []


def test_broken_sentiment_score_without_citations(broken_sentiment_score_without_citations):
    with pytest.raises(ValidationError) as val_error:
        Sentiment(**broken_sentiment_score_without_citations)
    
    citations_error = val_error.value.errors()[0]
    assert citations_error["type"] == 'value_error', "score must have citations"


def test_broken_sentiment_citations_without_score(broken_sentiment_citations_without_score, correct_citation):
    with pytest.raises(ValidationError) as val_error:
        Sentiment(**broken_sentiment_citations_without_score)
    
    citations_error = val_error.value.errors()[0]
    assert citations_error["type"] == 'value_error', "citations must have score"
