import re
import json

from elections.prompts.templates.user_prompt import USER_PROMPT_TEMPLATE
from elections.prompts.templates.utils import get_aliases


TITLE = """
Pedro Nuno Santos e Luís Montenegro: quem teve melhor nota no debate?
"""

DESCRIPTION = TITLE

TEXT = """
Maria João Avillez “Luís Montenegro manteve aquilo que faz dele um confiável primeiro-ministro. Foi mais claro, mais \
confiável na parte da habitação e do cenário macroeconómico. No entanto, vimos um Pedro Nuno Santos como nunca \
tínhamos visto até aqui”.

Ricardo Costa “No início do debate passou-se uma coisa grave. O debate foi feito com polícia à porta em protesto. \
Isto é absolutamente inaceitável. Pedro Nuno Santos disse: 'Eu não negoceio sobre coação', Montenegro ficou nas \
encolhas. Pedro Passos Coelho, Durão Barroso não teria dado esta resposta. NO primeiro minuto, Luís Montenegro \
perdeu o debate”.

Martim Silva “Pedro Nuno Santos entrou ao ataque. Tivemos 80 minutos, Pedro Nuno Santos marca no início do debate, \
todo o resto é equilibrado. O líder do PS teve dificuldades na habitação e saúde, mas no fim da partida volta a \
marcar golo na questão dos pensionistas”.

Alguem disse que Rui Rocha é um homano de sexo masculino. Rui Rocha vive em Portugal e que o secretado geral do PS \
estava nas cordas
"""

answer =  [
   {"name": "Luís Montenegro", "score": 0.5, "citations": [
      {"quote": "Luís Montenegro manteve aquilo que faz dele um confiável primeiro-ministro. Foi mais claro, mais \
         confiável na parte da habitação e do cenário macroeconómico", "score": 0.8, "author": "Maria João Avillez"},
      {"quote": "Montenegro ficou nas encolhas. Pedro Passos Coelho não teria dado esta resposta, Durão Barroso não \
         teria dado essa resposta, Cavaco Silva não teria dado essa resposta. NO primeiro minuto, Luís Montenegro \
            perdeu o debate", "score": 0.3, "author": "Ricardo Costa"},
    ]},
   {"name": "Pedro Nuno Santos", "score": 0.6, "citations": [\
      {"quote": "No entanto, vimos um Pedro Nuno Santos como nunca tínhamos visto até aqui", "score": 0.8,
         "author": "Maria João Avillez"}, \
      {"quote": "Pedro Nuno Santos entrou ao ataque. Tivemos 80 minutos, Pedro Nuno Santos marca no início do debate, \
         todo o resto é equilibrado", "score": 0.7, "author": "Martim Silva"},
      {"quote": "O líder do PS teve dificuldades na habitação e saúde, mas no fim da partida volta a marcar golo na \
         questão dos pensionistas", "score": 0.6, "author": "Martim Silva"},
      {"quote": "O secretado geral do PS estava nas cordas", "score": 0.2}]},
   {"name": "Rui Rocha", "score": None, "citations": []}
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
