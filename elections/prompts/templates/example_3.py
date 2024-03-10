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
"Entendi que não havia condições para manter Lidia Fernel" disse Mariana Mortágua.
"Queremos continuar a ter um governo do PS com problemas estruturais por resolver?. [Governos PS] Trouxeram a Portugal \
a maior crise do Estado Social de que há memória. Nunca os serviços públicos foram tão maltratados como nos últimos \
anos. Impostos máximos, serviços públicos mínimos."

O líder do André Ventura já tinha levantado a possibilidade na passada quinta-feira: em declarações aos jornalistas no \
Parlamento , Ventura afirmou que o partido ia investigar internamente o caso e que retiraria o ex-deputado do \
PSD se houvesse 'o mínimo vestígio de abuso ou de fraude'. 'Comigo não vão ter duas bitolas. Se isso acontecer, \
o deputado não estará nas listas do Chega, que ainda não foram entregues', afirmou. 

Reeleito com 98,9% dos votos, diz que a escolha se faz entre “o Portugal de 2024” do Chega e o de 1974, de Pedro Nuno Santos. Ataca ideologia de género e imigrantes islâmicos. 

Inês de Sousa Real acha que a Justiça na área do Direito Penal acha que ainda há muito a fazer e quer envolver todos \
os agentes. A defesa dos animais e da naturea continua a ser uma das suas bandeiras.

Depois das exigências na saúde e na educação, Rui Tavares pede agora um ministério da Agricultura capaz de dar \
resposta aos problemas dos pequenos agricultores e não apenas das grandes empresas do setor 

Com duas simples frases reequilibrou a favor do PS os danos morais do prometido chumbo ao governo dos Açores, onde o \
PSD precisa do Chega para formar maioria. O PAN já ão será suficiente.
"""

answer = [
    {"name": "Pedro Nuno Santos", "score": 0.3, "citations":[
        {"quote": "[Governos PS] Trouxeram a Portugal a maior crise do Estado Social de que há memória. Nunca os \
            serviços públicos foram tão maltratados como nos últimos anos. Impostos máximos, serviços públicos mínimos",
         "score": 0.3, "author": "Mariana Mortágua"},
        ]},
    {"name": "Mariana Mortágua", "score": None, "citations":[]},
    {"name": "André Ventura", "score": None, "citations":[]},
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
