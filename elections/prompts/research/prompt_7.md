# First prompt with pydantic and instructor
``` python

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
2. Break down passages: if a quote is conveying multiple pieces of information, break it down into smaller parts.
3. Filter Out Politicians: only keep extracts referring to people present on the provided politicians list.
4. Filter quotes: For each matched politician, attach in 'citations' all the corresponding quotes that contain an opinion (hence not just factual).
5. Scoring quotes: for each quote set a score from 0 to 1, with 1 being extremely good, .5 being neutral and 0 being extremely bad.
6. Author Attribution: If available, attribute quotes to their respective authors.
7. Final Score Calculation: Based on all extracted information, calculate a final score for each politician \
    reflecting the overall opinion. It should be aligned with the scoring of the quotes.
"""


USER_PROMPT = """\
ARTICLE:
\"""\
{article}\
\"""  

QUESTION: 
Only provide a JSON for your analysis and nothing more. The politicians score goes from 0 to 1. \
If the article is only contains factual information regarding a particular politician then the \
citations fields should be [] and the overall score should be: None 
"""
```



# On article 4
## sytem GPT-3.5 evaluation
[Sentiment(name='Pedro Nuno Santos', score=0.8, citations=[Citation(quote='Pedro Nuno Santos entrou ao ataque. A frase da autoridade do Estado, que podíamos esperar do líder de centro-direita, vem do ‘radical de esquerda’ como Montenegro gosta de o apelidar. Tivemos 80 minutos, Pedro Nuno Santos marca no início do debate, todo o resto é equilibrado. O líder do PS teve dificuldades na habitação e saúde, mas no fim da partida volta a marcar golo na questão dos pensionistas', score=0.8, author='Martim Silva'), Citation(quote='Expectativa jogou claramente a favor de Pedro Nuno Santos. Montenegro começou muito mal na questões das polícias. Não foi capaz de dizer à polícia para cumprir a lei e ordem. Na questão das pensões, Montenegro acabou por insistir numa coisa que não era verdade.', score=0.8, author='Paulo Baldaia'), Citation(quote='Foi uma belíssima performance de Pedro Nuno Santos, não só pelo início, mas também pelo fim. Consegue aguentar-se em temas tão curiosos como a governabilidade. Noutra das questões mais frágeis, Pedro Nuno Santos acaba por conseguir escapar - é o tema do aeroporto. Debate não podia ter corrido melhor a Pedro Nuno Santos, conseguiu agarra-lo no início e não foi fragilizado nas suas feridas mais abertas', score=0.8, author='Sebastião Bugalho')]),

 Sentiment(name='Luís Montenegro', score=0.1, citations=[Citation(quote='No início do debate passou-se uma coisa grave. O debate foi feito com polícia à porta em protesto. Isto é absolutamente inaceitável. Pedro Nuno Santos disse: ‘Eu não negoceio sobre coação’, Montenegro ficou nas encolhas. Pedro Passos Coelho não teria dado esta resposta, Durão Barroso não teria dado essa resposta, Cavaco Silva não teria dado essa resposta. NO primeiro minuto, Luís Montenegro perdeu o debate', score=0.1, author='Ricardo Costa'), Citation(quote="Pedro Nuno Santos esteve a descansar este tempo todo para ganhar balanço para este debate. Houve uma notícia aqui: Pedro Nuno desfez o tabu, inverteu as posições e disse uma frase que matou o assunto: 'não apresentaremos, nem votaremos favoravelmente moções de censura a um governo minoritário do PSD. Um dos problemas de Montenegro na questão da governabilidade, da PSP e do aeroporto foi não responde. Montenegro não arrancou bem", score=0.1, author='Daniel Oliveira'), Citation(quote='Pedro Nuno Santos não teve debates brilhantes, mas Pedro Nuno Santos perdeu este. Esteve quase sempre à defesa contra um animal político. Pedro Nuno Santos que andou empatado por uma série de questões, libertou-se. Talvez até se tenha liberta um pouco demais. Montenegro esteve mal no arranque', score=0.1, author='Ângela Silva')])]

 ## analysis
the actual grade for PNS: was 0.76 so 0.8 is very close, however for Montenegro although all commentators but one aggreed that his performance was worst (about 15pp then PNS) he had an overal score of 0.6 which is much higher then what GPT-3.5 gave him. It seems the seystem only captured the negatives about him and glanced over the positives 