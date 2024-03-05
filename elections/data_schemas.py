from typing_extensions import Annotated
from pydantic import BaseModel, Field, field_validator, ValidationInfo


Probability = Annotated[float, Field(strict=True, ge=0, le=1)]


class Citation(BaseModel):
    quote: str = Field(..., min_length=3)
    score: Probability
    author: str = Field(None, min_length=3, max_length=255)
    
    @field_validator('quote')
    @classmethod
    def validate_citation_exists(cls, quote: str, info: ValidationInfo) -> str:  
        context = info.context
        if context:
            context = context.get('article_n_meta')
            quote_in_article = any({quote in elem for elem in context})
            if not quote_in_article:
                raise ValueError(f"Citation `{quote}` not found in article_n_meta")
        return quote


# TODO: create a field_validator that ensures that score is in 
# [min Citation score, max Citation score] +/- 10%, if citations is not empty
class Sentiment(BaseModel):
    name: str
    score: float | None
    citations: list[Citation]

    @field_validator("citations")
    @classmethod
    def check_score_iff_citations(cls, citations, values) -> list[Citation]:
        score = values.data["score"]
        no_score_no_citations = score is None and not citations
        score_and_citations = score is not None and citations
        
        if no_score_no_citations or score_and_citations:
            return citations
        
        raise ValueError("Either both a score and citations are present\
            or neither are.")
    
    @field_validator("name")
    @classmethod
    def validate_name_in_article(cls, name: str, info: ValidationInfo) -> str:
        context = info.context
        if context:
            context = context.get('article_n_meta')
            politican_in_article = any({name in elem for elem in context})
            if not politican_in_article:
                raise ValueError(f"Citation `{name}` not found in article_n_meta")
        return name


class ArticleSentiment(BaseModel):
    sentiments: list[Sentiment]
    
    @field_validator("sentiments")
    @classmethod
    def validate_all_politicians_ided(cls, sentiments: str, info: ValidationInfo) -> str:
        context = info.context
        if context:
            politican_present = set(context.get('politicians_present'))
            politicians_retreived = {sentiment.name for sentiment in sentiments}
            if politicians_retreived != politican_present:
                politicians_missing = politican_present - politicians_retreived
                raise ValueError(f"This politicians weren't found: {politicians_missing}")
        return sentiments
