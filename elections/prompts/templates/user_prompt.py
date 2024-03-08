BASE_PROMPT = """
## ARTICLE
\"""
### Title
{title}

### Description
{description}

### Text
{text}
\"""

## ALIASES
{aliases}
"""


USER_PROMPT = """
{base_prompt}

# QUESTION
These politicians are present in the article: {names} either directly or via aliases and must appear in your output. \
For each of them provide a JSON for your analysis and nothing more. The politicians score goes from 0 to 1. \
If the article is only contains factual information regarding a particular politician then the citations \
fields should be [] and the overall score should be: None

## ANSWER:
""".format(base_prompt=BASE_PROMPT, names="{names}")


EXAMPLE_PROMPT = """
{base_prompt}

## ANSWER:
{answer}
""".format(base_prompt=BASE_PROMPT, answer="{answer}")
