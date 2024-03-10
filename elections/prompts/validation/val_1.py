import re
import json

from elections.prompts.templates.user_prompt import USER_PROMPT_TEMPLATE
from elections.prompts.templates.utils import get_aliases


TITLE = """
A vida na campanha legislativa 2024
"""

DESCRIPTION = """
Multiplas ideias e commentarios dos candidatos à presidência do governo de Portugal.
"""

TEXT = """
Inês Sousa Real acha que a Justiça na área do Direito Penal acha que ainda há muito a fazer e quer envolver todos \
os agentes. A defesa dos animais e da naturea continua a ser uma das suas bandeiras.

Depois das exigências na saúde e na educação, Rui Tavares pede agora um ministério da Agricultura capaz de dar \
resposta aos problemas dos pequenos agricultores e não apenas das grandes empresas do setor 

Com duas simples frases reequilibrou a favor do PS os danos morais do prometido chumbo ao governo dos Açores, onde o \
PSD precisa do Chega para formar maioria. O PAN já ão será suficiente.
"""

answer = [
    {"name": "Inês de Sousa Real", "score": None, "citations":[]},
    {"name": "Rui Tavares", "score": None, "citations":[]}
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