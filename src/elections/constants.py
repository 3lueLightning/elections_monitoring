import logging

from pathlib import Path
from datetime import datetime


# Folders
PACKAGE_ROOT = Path(__file__).parents[2]
SRC_FOLDER = PACKAGE_ROOT / "elections"
LOG_DIR = PACKAGE_ROOT / "logs"
DATA_DIR = PACKAGE_ROOT / "data"
RAW_DATA_DIR = DATA_DIR / "raw"
INTERIM_DATA_DIR = DATA_DIR / "interim"
PROCESSED_DATA_DIR = DATA_DIR / "processed"

# NewsFinder params
COUNTRY = "PT"
LANGUAGE = "pt"
NEWS_DB = INTERIM_DATA_DIR / "news.sqlite"

# Parties scraping
POLITICAL_PATHS = {
    "psd": RAW_DATA_DIR / "psd" / "proposals.tsv"
}

# OpenAI API
MAX_RETRIES = 3
OPENAI_GPT_MODEL = 'gpt-3.5-turbo' # 'gpt-4-turbo-preview'

# Logging
LOG_LVL = logging.INFO
SCRAPE_LOG_FN = LOG_DIR / "scrape.log"
SENTIMENT_LOG_FN = LOG_DIR / "sentiment.log"
RESULTS_LOG_FN = LOG_DIR / "results.log"

# Portuguese news outlets
NEWS_OUTLETS = [
    "Público",
    "Correio da Manhã",
    "Jornal de Notícias",
    "Expresso",
    "Diário de Notícias",
    "Observador",
    "Sábado",
    "SIC Noticias",
    "RTP Noticias",
    "TSF",
    "Renascença",
    "Sol",
    "Eco",
    "TVI",
    "TVI24",
    "Visão",
    "noticias de coimbra",
    "porto canal",
    "Madeira",
    "SAPO",
    "SAPO24",
    "Açores"
]

# Politicians
POLITICIAN_ALIASES = {
    "Pedro Nuno Santos": [
        "líder do PS",
        "líder do P.S.",
        "líder do Partido Socialista",
        "secretário-geral do PS",
    ],
    "Luís Montenegro": [
        "Montenegro",
        "presidente do PSD",
        "presidente do P.S.D.",
        "presidente do Partido Social Democrata",
    ],
    "André Ventura": [
        "Ventura",
        "presidente do Chega",
        "líder do Chega",
    ],
    "Rui Rocha": [
        "presidente da IL",
        "presidente da Iniciativa Liberal",
        "líder dos Liberais"
    ],
    "Mariana Mortágua": [
        "Mortágua",
        "coordenadora do BE",
        "coordenadora do Bloco de Esquerda",   
    ],
    "Paulo Raimundo": [
        "Raimundo",
        "secretário-geral do PCP",
        "representante da CDU",
    ],
    "Inês de Sousa Real": [
        "Inês Sousa Real",
        "Sousa Real",
        "porta voz do PAN",
        "porta voz do Partido Aniamis e Natureza",
    ],
    "Rui Tavares": [
        "líder do Livre",
        "líder do partido Livre",
    ],
}
SURNAMES = {
    "Pedro Nuno Santos": "Nuno Santos",
    "Luís Montenegro": "Montenegro",
    "André Ventura": "Ventura",
    "Rui Rocha": "Rocha",
    "Mariana Mortágua": "Mortágua",
    "Paulo Raimundo": "Raimundo",
    "Inês de Sousa Real": "Sousa Real",
    "Rui Tavares": "Tavares",
}
POLITICIANS = list(POLITICIAN_ALIASES.keys())

POLITICIAN_COLORS = {
    "Pedro Nuno Santos": "#D32329",# "#139E6A",
    "Luís Montenegro": "#F37F27",
    "André Ventura": "#1F1F4C",
    "Rui Rocha": "#04ADEF",
    "Mariana Mortágua": "#e11b22",
    "Paulo Raimundo": "#035FBC",
    "Inês de Sousa Real": "#01798E",
    "Rui Tavares": "#C3D500",
}

PARTIES = {
    "Pedro Nuno Santos": "secretário-geral do PS",
    "Luís Montenegro": "presidente do partido social democrate (PSD) e lider da AD",
    "André Ventura": "presidente do Chega",
    "Rui Rocha": "presidente da Iniciativa Liberal (IL)",
    "Mariana Mortágua": "coordenadora do Bloco de Esquerda (BE)",
    "Paulo Raimundo": "secretário-geral do PCP e lider da CDU",
    "Inês de Sousa Real": "porta voz do Partido Animais e Natureza (PAN)",
    # HOTFIX
    "Inês Sousa Real": "porta voz do Partido Animais e Natureza (PAN)",
    "Rui Tavares": "líder do Livre",
}

PM_RESIGNATION_DATE = datetime(2023, 12, 7, 0, 0, 0)
