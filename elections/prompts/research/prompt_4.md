# Article 1
## Prompt
SYSTEM  
You will be provided with a document delimited by triple quotes and a question. Your task is to answer the question using only the provided document and to cite the passage(s) of the document used to answer the question. If the document does not contain the information needed to answer this question, then simply write: {}. If an answer to the question is provided, it must be in the following JSON format, the terms surrounded by < > are variables: [{“name”: <politician name>, “score”: <the score you determined>, “citations”: {“citation”: <citation 1>, “positive_proba”: <probability>}]}] .

Take your time to answer the question and go through the following steps:
1.	identify the politicians in the article
2.	for each politician identify the parts of the article that refer to them
3.	for each part determine the probability that it is good
4.	for all parts that contain an opinion include them in the citations of the corresponding politician and indicate the probability of it being positive in the field positive_proba 
5.	based on all the citations you identified provide a final score to the politician that reflects the overall opinion

USER  
""" 
Luís Montenegro e André Ventura: quem teve melhor nota no debate? Na análise ao desempenho dos líderes da AD e do Chega no debate desta segunda-feira, Bernardo Ferrão e Sebastião Bugalho consideram que Luís Montenegro brincou com André Ventura e o pôs no devido lugar e que o líder do Chega esteve mais moderado, mas não foi coerente. Bernardo Ferrão “Este era um debate difícil e importante para os dois candidatos, uma vez que este combate na direita está com muitas provas de força em ambos. Parece que Luís Montenegro conseguiu mostrar que André Ventura não é uma pessoa coerente, é alguém que muda muitas vezes de opinião. Achei André Ventura nervoso neste debate. Não esteve completamente à vontade. André Ventura não teve a atitude de interromper constantemente, esteve mais controlado.” Sebastião Bugalho “Luís Montenegro tinha claramente uma estratégia, percebeu-se que era não levar muito a sério André Ventura. Ele não se enerva com André Ventura, não levanta a voz. Até parecia que estava a brincar com ele. Foi o primeiro líder partidário que enfrentou André Ventura e que o tratou exatamente como ele é, alguém incoerente que tem 7,18% do resultado das últimas eleições” 
"""  

Question: Only provide a JSON for your analysis and nothing more. The politicians score goes from 1 to 5 (with 1 being extremely bad). If the opinion is neutral provide a 3, if the article is only factual and does not have an opinion then the score should be None. 

## Answer

[{"name": "Luís Montenegro", "score": 4, "citations": {"citation": "Na análise ao desempenho dos líderes da AD e do Chega no debate desta segunda-feira, Bernardo Ferrão e Sebastião Bugalho consideram que Luís Montenegro brincou com André Ventura e o pôs no devido lugar... alguém incoerente que tem 7,18% do resultado das últimas eleições”", "positive_proba": 0.8}},
{"name": "André Ventura", "score": 2, "citations": {"citation": "“Este era um debate difícil e importante para os dois candidatos... Achei André Ventura nervoso neste debate. Não esteve completamente à vontade. André Ventura não teve a atitude de interromper constantemente, esteve mais controlado.”", "positive_proba": 0.2}}]

## Evaluation
Great




# Article 2
## Prompt
SYSTEM  
You will be provided with a document delimited by triple quotes and a question. Your task is to answer the question using only the provided document and to cite the passage(s) of the document used to answer the question. If the document does not contain the information needed to answer this question, then simply write: {}. If an answer to the question is provided, it must be in the following JSON format, the terms surrounded by < > are variables: [{“name”: <politician name>, “score”: <the score you determined>, “citations”: {“citation”: <citation 1>, “positive_proba”: <probability>}]}] .

Take your time to answer the question and go through the following steps:
1.	identify the politicians in the article
2.	for each politician identify the parts of the article that refer to them
3.	for each part determine the probability that it is good
4.	for all parts that contain an opinion include them in the citations of the corresponding politician and indicate the probability of it being positive in the field positive_proba 
5.	based on all the citations you identified provide a final score to the politician that reflects the overall opinion

USER  
""" 
Mariana Rodrigues Mortágua (Alvito, Alvito, 24 de junho de 1986) é uma economista e política portuguesa do partido Bloco de Esquerda. Atualmente, desempenha as funções de Coordenadora Nacional do Bloco de Esquerda, deputada na Assembleia da República e vice-presidente do grupo parlamentar.[1]
Biografia
Filha de Camilo Mortágua, histórico ativista antisalazarista, revolucionário, membro fundador e operacional da LUAR, é irmã gémea da também dirigente e deputada do Bloco de Esquerda Joana Mortágua e prima afastada da socialista Maria João Rodrigues.[2]
É licenciada e mestre em Economia, pelo ISCTE - Instituto Universitário de Lisboa, tendo terminado o doutoramento em Economia[1] na School of Oriental and African Studies (SOAS) da Universidade de Londres.[3] A sua dissertação de mestrado e a sua tese de doutoramento assentam em perspectivas críticas dentre da Economia Política e ambas desenvolvem aspectos diferentes da crise económica de 2008 e a estagnação económica da década seguinte, em particular em Portugal.[4][5] Em 2022, conclui ainda uma pós-graduação em Gestão Fiscal Avançada, no ISEG.[6] Mariana foi professora no ISCAL no ano lectivo 2011-2012[7] e, desde 2021, é professora auxiliar no ISCTE.[8]
Militante do Bloco de Esquerda desde 2007, estreou-se como deputada na Assembleia da República aos 27 anos, em 2013, por necessidade de substituição de Ana Drago no círculo eleitoral de Lisboa, onde foi eleita. A sua nomeação em setembro de 2013 para os lugares cimeiros da lista de candidatos a deputados por parte da Comissão Política do BE foi contestada por um grupo de militantes, que criticaram o "critério tecnocrata" que orientou a sua escolha, nomeadamente o facto de ter conhecimentos de economia. Perante isto, o BE confirmou que Mariana Mortágua foi considerada como o elemento que “melhor serviria os interesses do partido na Assembleia da República, em virtude dos seus conhecimentos na área da Economia”, algo que se vinha “a fazer sentir desde a saída de Francisco Louçã”.[9]
Mariana Mortágua foi eleita deputada à Assembleia Municipal de Lisboa, pelo Bloco de Esquerda, em 2013[10] e foi reeleita deputada nas Eleições Legislativas de 2015, que deram ao Bloco de Esquerda a sua maior votação de sempre.[11] Integrou a Comissão de Economia e Obras Públicas, a Comissão de Orçamento, Finanças e Administração Pública e a Comissão Eventual para Acompanhamento das Medidas do Programa de Assistência Financeira a Portugal. Foi de novo reeleita deputada em outubro de 2019 e em janeiro de 2022.[1]
"""  

Question: Only provide a JSON for your analysis and nothing more. The politicians score goes from 1 to 5 (with 1 being extremely bad). If the opinion is neutral provide a 3, if the article is only factual and does not have an opinion then the score should be None. 


## Answer
[{"name": "Mariana Rodrigues Mortágua", "score": None, "citations": {}}]


## Evaluation
Almost perfect the it should have been `"citations": []`
