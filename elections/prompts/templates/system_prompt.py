from elections.prompts.templates import example_1


SYSTEM_PROMPT = """\
# TASK
You will be provided with a document delimited by triple quotes and a question. \
Your task is to answer the question using only the provided document and to cite \
the passage(s) of the document used to answer the question. If the document does \
not contain the information needed to answer this question, then simply write: [].

## PROCESS
Take your time to answer the question and go through the following steps:
1. 
1. Parse Document: Extract relevant information from the document, such as quotes and mentions of the politicians
   provided by the user
2. Break down passages: if a quote is conveying multiple pieces of information, break it down into smaller parts.
3. Preserve quotes: never alter a passage, even it there are spelling or grammatical mistakes. If you skip part of the
   text then use ... to indicate the skipped part.
4. Filter quotes: For each matched politician, attach in 'citations' all the corresponding quotes that contain an
   opinion (hence not just factual).
5. Scoring quotes: for each quote set a score from 0 to 1, with 1 being extremely good, .5 being neutral and 0 being
   extremely bad.
6. Author Attribution: If available, attribute quotes to their respective authors.
7. Final Score Calculation: Based on all extracted information, calculate a final score for each politician
   reflecting the overall opinion. It should be aligned with the scoring of the quotes.

------------------------------
# EXAMPLE 1:
{example_1}

""".format(example_1=example_1.EXAMPLE)