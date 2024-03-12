import numpy as np

from typing import Optional

from thefuzz import fuzz
from typing_extensions import Annotated
from pydantic import BaseModel, Field, field_validator, ValidationInfo

from elections import constants

Probability = Annotated[float, Field(strict=True, ge=0, le=1)]


class Citation(BaseModel):
    quote: str = Field(..., min_length=3)
    score: Probability
    author: Optional[str] = Field(None, min_length=3, max_length=255)
    
    @field_validator('quote')
    @classmethod
    def validate_citation_exists(cls, quote: str, info: ValidationInfo) -> str:  
        context = info.context
        if context:
            article_n_meta = context.get('article_n_meta')
            quote_pieces = quote.split("...")
            piece_match_ratio = np.array([fuzz.partial_ratio(piece, article_n_meta) for piece in quote_pieces])
            w = np.array([len(piece) for piece in quote_pieces]) / len(quote)
            match_ratio = np.sum(w * piece_match_ratio)
            if match_ratio < 60:
                raise ValueError(f"Citation `{quote}` not found in article_n_meta, match_ratio: {match_ratio}")
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
            article_n_meta = context.get('article_n_meta')
            # HOTFIX Ines de Sousa Real
            surnames = constants.SURNAMES.get(name, name)
            if surnames not in article_n_meta:
                raise ValueError(f"Citation `{surnames}` not found in article_n_meta")
        return name


class ArticleSentiment(BaseModel):
    sentiments: list[Sentiment]
    
    """
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
    """
