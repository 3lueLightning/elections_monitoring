SYSTEM_PROMPT = """\
TASK
You will be provided with a document delimited by triple quotes and a question. \
Your task is to answer the question using only the provided document and to cite \
the passage(s) of the document used to answer the question. If the document does \
not contain the information needed to answer this question, then simply write: [].

ADDITIONAL INFORMATION
Politicians list: {politicians}

PROCESS
Take your time to answer the question and go through the following steps:
1. Parse Document: Extract relevant information from the document, such as quotes and mentions of politicians.
2. Identify Politicians: Match mentioned politicians from the provided list with those mentioned in the document.
3. Quote Extraction: For each matched politician, extract quotes that refer to them.
4. Opinion Analysis: Analyze the extracted quotes for sentiment or opinion, if applicable, and include this information in the citations.
5. Author Attribution: If available, attribute quotes to their respective authors and include this information in the citations.
6. Final Score Calculation: Based on all extracted information, calculate a final score for each politician reflecting the overall opinion.
7. JSON Generation: Generate the final JSON output, including only information relevant to mentioned politicians.
"""


USER_PROMPT = """\
ARTICLE:
\"""\
{article}\
\"""  

QUESTION: 
Only provide a JSON for your analysis and nothing more. \
The politicians score goes from 0 to 1 (with 1 being extremely good). \
If the opinion is neutral provide a .5, if the article is only factual \
and does not have an opinion then the score should be: None 
"""

bkp = """
1.	consider this list of politicians: {politicians}
2.	for each politicians present identify all the quotes of the article that refer to them
3.	for all parts that contain an opinion include them in the citations of the \
    corresponding politician and indicate the probability of it being positive \
    in the field score in the citations
4.  if possible indicate the author of the quote in the citations
5.	based on all the citations you have identified provide a final score to the \
    politician that reflects the overall opinion
6.  if a politician is mentioned in the article, but there are no quotes about him just leave \
    the citations field empty.
7.  If a politician isn't mentioned in the article do not include them under any circumstances \
    in the final JSON !
"""