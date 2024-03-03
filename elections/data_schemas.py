from typing import Iterable
from typing_extensions import Annotated
from pydantic import BaseModel, Field, field_validator


Probability = Annotated[float, Field(strict=True, ge=0, le=1)]


class Citation(BaseModel):
    quote: str = Field(..., min_length=3)
    score: Probability
    author: str = Field(None, min_length=3, max_length=255)


class Sentiment(BaseModel):
    name: str
    score: float | None
    citations: list[Citation]

    @field_validator("citations")
    def check_score_iff_citations(cls, citations, values):
        score = values.data["score"]
        no_score_no_citations = score is None and not citations
        score_and_citations = score is not None and citations
        
        if no_score_no_citations or score_and_citations:
            return citations
        
        raise ValueError("Either both a score and citations are present\
            or neither are.")

    # TODO: create a field_validator that ensures that score is in 
    # [min Citation score, max Citation score] +/- 10%, if citations is not empty
    
    # TODO: validate that the politicians mentioned are in the article
    
    # TODO: create llm validator to ensure that the citation are in the orginal text

ArticleSentiment = Iterable[Sentiment]
