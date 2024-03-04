import re

from elections import constants


example_answer = """
[{{"name": "Luís Montenegro", "score": 0.5, "citations": [\
    {{"quote": "Luís Montenegro manteve aquilo que faz dele um confiável primeiro-ministro. Foi mais claro, mais confiável \
        na parte da habitação e do cenário macroeconómico", "score": 0.8, "author": "Maria João Avillez"}}, \
    {{"quote": "Montenegro ficou nas encolhas. Pedro Passos Coelho não teria dado esta resposta, Durão Barroso não teria \
        dado essa resposta, Cavaco Silva não teria dado essa resposta. NO primeiro minuto, Luís Montenegro perdeu o debate", \
        "score": 0.3, "author": "Ricardo Costa"}}, \
    ]}}, \
 {{"name": "Pedro Nuno Santos", "score": 0.6, "citations": [\
    {{"quote": "No entanto, vimos um Pedro Nuno Santos como nunca tínhamos visto até aqui", "score": 0.8, \
        "author": "Maria João Avillez"}}, \
    {{"quote": "Pedro Nuno Santos entrou ao ataque. Tivemos 80 minutos, Pedro Nuno Santos marca no início do debate, \
        todo o resto é equilibrado", "score": 0.7, "author": "Martim Silva"}}, \
    {{"quote": "O líder do PS teve dificuldades na habitação e saúde, mas no fim da partida volta a marcar golo na \
        questão dos pensionistas", "score": 0.6, "author": "Martim Silva"}}, \
    {{"quote": "O secretado geral do PS estava nas cordas", "score": 0.2}}]}}, \
 {{"name": "Rui Rocha", "score": None, "citations": []}}]
"""

EXAMPLE_ANSWER = re.sub(r'\s+', ' ', example_answer.strip())


SYSTEM_PROMPT = """\
# TASK
You will be provided with a document delimited by triple quotes and a question. \
Your task is to answer the question using only the provided document and to cite \
the passage(s) of the document used to answer the question. If the document does \
not contain the information needed to answer this question, then simply write: [].

## ADDITIONAL INFORMATION
Politicians list: {politicians}

## PROCESS
Take your time to answer the question and go through the following steps:
1. Parse Document: Extract relevant information from the document, such as quotes and mentions of politicians.
2. Break down passages: if a quote is conveying multiple pieces of information, break it down into smaller parts.
3. Filter Out Politicians: only keep extracts referring to people present on the provided politicians list.
4. Filter quotes: For each matched politician, attach in 'citations' all the corresponding quotes that contain an opinion
   (hence not just factual).
5. Scoring quotes: for each quote set a score from 0 to 1, with 1 being extremely good, .5 being neutral and 0 being
   extremely bad.
6. Author Attribution: If available, attribute quotes to their respective authors.
7. Final Score Calculation: Based on all extracted information, calculate a final score for each politician
   reflecting the overall opinion. It should be aligned with the scoring of the quotes.

------------------------------
# EXAMPLE 1:
## ARTICLE
\"""
### Title
Pedro Nuno Santos e Luís Montenegro: quem teve melhor nota no debate?

### Description
Pedro Nuno Santos e Luís Montenegro: quem teve melhor nota no debate? 

### Text
Maria João Avillez “Luís Montenegro manteve aquilo que faz dele um confiável primeiro-ministro. Foi mais claro, mais confiável\
na parte da habitação e do cenário macroeconómico. No entanto, vimos um Pedro Nuno Santos como nunca tínhamos visto até aqui”.

Ricardo Costa “No início do debate passou-se uma coisa grave. O debate foi feito com polícia à porta em protesto. \
Isto é absolutamente inaceitável. Pedro Nuno Santos disse: 'Eu não negoceio sobre coação', Montenegro ficou nas encolhas. \
Pedro Passos Coelho, Durão Barroso não teria dado esta resposta. NO primeiro minuto, Luís Montenegro perdeu o debate”.

Martim Silva “Pedro Nuno Santos entrou ao ataque. Tivemos 80 minutos, Pedro Nuno Santos marca no início do debate, todo \
o resto é equilibrado. O líder do PS teve dificuldades na habitação e saúde, mas no fim da partida volta a marcar golo na \
questão dos pensionistas”.

Alguem disse que Rui Rocha é um homano de sexo masculino. Rui Rocha vive em Portugal e que o secretado geral do PS estava \
nas cordas
\"""

## Answer:
{example_answer}

""".format(example_answer=EXAMPLE_ANSWER, politicians=constants.POLITICIANS)


USER_PROMPT = """\
# ARTICLE:
\"""\
## Title
{title}

## Description
{description}

## Text
{text}
\"""  

# QUESTION: 
Only provide a JSON for your analysis and nothing more. The politicians score goes from 0 to 1. \
If the article is only contains factual information regarding a particular politician then the \
citations fields should be [] and the overall score should be: None 
"""
