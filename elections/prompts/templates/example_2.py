import re
import json

from elections.prompts.templates.user_prompt import USER_PROMPT_TEMPLATE
from elections.prompts.templates.utils import get_aliases


TITLE = """
Paulo Raimundo considera que o PS de Pedro Nuno Santos é igual ao de António Costa - SIC Notícias
"""

DESCRIPTION = TITLE

TEXT = """
Aqui houve divisão: uns deram vitória a Ventura, outros a Raimundo. Mas todos concordaram nisto: foi um debate \
abaixo da linha de água: 3 para o PCP, 2,6 para o Chega. 

Paulo Raimundo esteve este sábado no distrito de Beja, num Alentejo que ainda ajuda a CDU a eleger deputados. \
Para lá chegar, o líder da CDU seguiu pelo IP8 e aproveitou para apontar responsabilidades a Pedro Nuno Santos, \
enquanto ex-ministro das Infraestruturas, pela falta de conclusão de obras no itinerário principal que atravessa \
o Baixo Alentejo.
"""

answer = [
    {"name": "Pedro Nuno Santos", "score": 0.4, "citations":[
        {"quote": "o PS de Pedro Nuno Santos é igual ao de António Costa",
         "score": 0.4, "author": "Paulo Raimundo"},
        {"quote": "aproveitou para apontar responsabilidades a Pedro Nuno Santos, enquanto ex-ministro das \
            Infraestruturas, pela falta de conclusão de obras no itinerário principal que atravessa o Baixo Alentejo.",
            "score": 0.4, "author": "Paulo Raimundo"}]},
    {"name": "André Ventura", "score": 0.5, "citations":[
        {"quote": "uns deram vitória a Ventura, outros a Raimundo. Mas todos \
            concordaram nisto: foi um debate abaixo da linha de água: 3 para o PCP, 2,6 para o Chega",
            "score": 0.5}]},
    {"name": "Paulo Raimundo", "score": 0.6, "citations":[
        {"quote": "uns deram vitória a Ventura, outros a Raimundo. Mas todos \
          concordaram nisto: foi um debate abaixo da linha de água: 3 para o PCP, 2,6 para o Chega",
         "score": 0.6}]}
]
answer_json = json.dumps(answer, ensure_ascii=False)
ANSWER = re.sub(r'\s+', ' ', answer_json.strip())

POLITICIANS = [sentiment["name"] for sentiment in answer]

EXAMPLE_PROMPT = USER_PROMPT_TEMPLATE.format(
   title=TITLE,
   description=DESCRIPTION,
   text=TEXT,
   answer=ANSWER,
   aliases=get_aliases(POLITICIANS),
   names=", ".join(POLITICIANS),
)
