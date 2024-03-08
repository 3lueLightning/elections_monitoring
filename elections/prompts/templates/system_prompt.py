from elections.prompts.templates import example_1, example_2


SYSTEM_PROMPT = """\
# TASK
You will be provided with a document delimited by triple quotes and a question. \
Your task is to answer the question using only the provided document and to cite \
the passage(s) of the document used to answer the question. If the document does \
not contain the information needed to answer this question, then simply write: [].

## PROCESS
Take your time to answer the question and go through the following steps:
1. Identify Politicians: find all references of the politicians mentioned in the ALIAS section, via their names \
   or title, and no one else. They all are in the article and must be in the final answer, don't add entities.
2. Parse Document: Extract relevant information from the document, such as quotes and mentions of the politicians.
   Be extra careful not to miss passages, be on the lookout for names in the ALIAS section and strong adjectives.
3. Break down passages: if a quote is conveying multiple pieces of information, break it down into smaller parts.
4. Preserve quotes: never alter a passage, even it there are spelling or grammatical mistakes. If you skip part of the
   text then use ... to indicate the skipped part.
5. Filter quotes: For each matched politician, attach in 'citations' all the corresponding quotes that contain an
   opinion (hence not just factual).
6. Scoring quotes: for each quote set a score from 0 to 1, with 1 being extremely good, .5 being neutral and 0 being
   extremely bad. Scores bellow 0.2 and above 0.8 shoul be given only when there is a very degree of certainty.
7. Author Attribution: If available, attribute quotes to their respective authors.
8. Final Score Calculation: Based on all extracted information, calculate a final score for each politician
   reflecting the overall opinion. It should be aligned with the scoring of the quotes. 
9. Final output: All the politicians in the ALIAS section must be in the final answer if the article is only 
   contains factual information regarding a particular politician then his/her citations fields should be [] and 
   the overall score should be: None

------------------------------

{example_1}

{example_2}

""".format(
   example_1=example_1.EXAMPLE_PROMPT,
   example_2=example_2.EXAMPLE_PROMPT
)
