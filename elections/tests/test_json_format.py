import json

from elections.utils import escape_quotes_within_citation

 
def test_quotes_within_string():
    input_string = """\
    [{"name": "Luís Montenegro", "score": 3, "citations": []}, \
    {"name": "Pedro Nuno Santos", "score": 2, "citations": \
    [{"citation": "O líder do PSD lembrou que tanto José Luís Carneiro \
    como Pedro Nuno Santos "fizeram parte dos governos de António Costa" \
    que, segundo a sua avaliação, tiveram "muito pouco investimento público".", \
    "positive_proba": 0.4}]}]"""
    
    assert json.loads(escape_quotes_within_citation(input_string)), \
        "didn't escape quotes within citation"
