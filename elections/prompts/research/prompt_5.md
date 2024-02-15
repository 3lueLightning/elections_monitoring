# Article 3
## Prompt

``` python
import re


json_format = """\
[
    {
        "name": "<politician name>",
        "score": <the score you determined>,
        "citations": [
            {
                "citation": "<citation 1>",
                "positive_proba": <probability>
            }
        ]
    }
]
"""
JSON_FORMAT = re.sub(r"\n\s*", "", json_format)


SYSTEM_PROMPT = """\
TASK
You will be provided with a document delimited by triple quotes and a question. \
Your task is to answer the question using only the provided document and to cite \
the passage(s) of the document used to answer the question. If the document does \
not contain the information needed to answer this question, then simply write: {{}}.\
If an answer to the question is provided, it must be in the following JSON format, \
the terms surrounded by < > are variables: {json_format}

PROCESS
Take your time to answer the question and go through the following steps:
1.	consider this list of politicians: {politicians}
2.  identify which of them are mentioned in the article, if there not do not include them
3.	for each politician identify the parts of the article that refer to them
4.	for each part determine the probability that it is good
5.	for all parts that contain an opinion include them in the citations of the\
    corresponding politician and indicate the probability of it being positive\
    in the field positive_proba 
6.	based on all the citations you identified provide a final score to the\
    politician that reflects the overall opinion
"""


USER_PROMPT = """\
ARTICLE:
\"""\
{article}\
\"""  

QUESTION: 
Only provide a JSON for your analysis and nothing more. \
The politicians score goes from 1 to 5 (with 1 being extremely bad). \
If the opinion is neutral provide a 3, if the article is only factual \
and does not have an opinion then the score should be "None". 
"""
```

## Answer
'[{"name": "Luís Montenegro", "score": 3, "citations": []},\n {"name": "Pedro Nuno Santos", "score": 3, "citations": []}]'

# Evaluation
