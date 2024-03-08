import pytest

from elections.data_schemas import Citation, Sentiment, ArticleSentiment


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
        "name": "André Ventura", 
        "score": 0.4, 
        "citations":[correct_citation]
    }
    return sentiment


@pytest.fixture
def correct_sentiment_without_score():
    sentiment = {
        "name": "Luís Montenegro", 
        "score": None, 
        "citations":[]
    }
    return sentiment


@pytest.fixture
def broken_sentiment_score_without_citations():
    sentiment = {
        "name": "Rui Tavares", 
        "score": .6, 
        "citations":[]
    }
    return sentiment


@pytest.fixture
def broken_sentiment_citations_without_score(correct_citation):
    sentiment = {
        "name": "Mariana Mortágua", 
        "score": None, 
        "citations":[correct_citation]
    }
    return sentiment    


def test_correct_citation(correct_citation):
    citation = Citation(**correct_citation)
    assert citation.quote == "some slightly negative quote"
    assert citation.score == 0.4


def test_broken_citation(broken_citation):
    with pytest.raises(ValueError) as val_error:
        Citation(**broken_citation)
    
    (quote_error, proba_error) = val_error.value.errors()
    assert quote_error["type"] == 'string_too_short', "quote must have multiple characters"
    assert proba_error["type"] == 'less_than_equal', "score must be between 0 and 1"


def test_correct_sentiment_with_score(correct_sentiment_with_score, correct_citation):
    sentiment = Sentiment(**correct_sentiment_with_score)
    sentiment.name == "André Ventura"
    sentiment.score == 0.4
    sentiment.citations == [correct_citation]


def test_correct_sentiment_without_score(correct_sentiment_without_score):
    sentiment = Sentiment(**correct_sentiment_without_score)
    sentiment.name == "Luís Montenegro"
    sentiment.score == None
    sentiment.citations == []


def test_broken_sentiment_score_without_citations(broken_sentiment_score_without_citations):
    with pytest.raises(ValueError) as val_error:
        Sentiment(**broken_sentiment_score_without_citations)
    
    citations_error = val_error.value.errors()[0]
    assert citations_error["type"] == 'value_error', "score must have citations"


def test_broken_sentiment_citations_without_score(broken_sentiment_citations_without_score):
    with pytest.raises(ValueError) as val_error:
        Sentiment(**broken_sentiment_citations_without_score)
    
    citations_error = val_error.value.errors()[0]
    assert citations_error["type"] == 'value_error', "citations must have score"


def test_citation_exists(correct_citation):
    cite = Citation.model_validate(
        correct_citation,
        context={"article_n_meta": "Here is some slightly negative quote, oh my!"},  
    )
    assert Citation(**correct_citation) == cite, "should have passed validation"


def test_citation_not_exists(correct_citation):
    with pytest.raises(ValueError):
        Citation.model_validate(
            correct_citation,
            context={"article_n_meta": "Some different talks"},  
        )


def test_name_in_article(correct_sentiment_with_score):
    sentiment = Sentiment.model_validate(
        correct_sentiment_with_score,
        context={"article_n_meta": "O André Ventura debateu de varios temas com Mariana Mortágua.\
            Then some slightly negative quote."},  
    )
    assert Sentiment(**correct_sentiment_with_score) == sentiment, "should have passed validation"


def test_name_not_in_article(correct_sentiment_with_score):
    with pytest.raises(ValueError):
        Sentiment.model_validate(
            correct_sentiment_with_score,
            context={"article_n_meta": ["O Luís Montenegro debateu de varios temas com Mariana Mortágua.\
                Then some slightly negative quote."]},  
        )


def inactive_test_article_sentiment_all_politicians_ided(
        correct_sentiment_with_score, correct_sentiment_without_score):
    sentiments = [
            Sentiment(**correct_sentiment_with_score),
            Sentiment(**correct_sentiment_without_score),
        ]
    atc_s = ArticleSentiment.model_validate(
        {"sentiments": sentiments},
        context={
            "politicians_present": ["André Ventura", "Luís Montenegro"]
        },  
    )
    assert ArticleSentiment(sentiments=sentiments) == atc_s, "should have passed validation"


def inactive_test_article_sentiment_some_politicians_missing(correct_sentiment_without_score):
    sentiments = [
            Sentiment(**correct_sentiment_without_score),
        ]
    with pytest.raises(ValueError):
        ArticleSentiment.model_validate(
            {"sentiments": sentiments},
            context={
                "politicians_present": ["André Ventura", "Luís Montenegro"]
            },  
        )
    