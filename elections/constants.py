import logging

from pathlib import Path
from datetime import datetime

from milvus import default_server


# Folders
PACKAGE_ROOT = Path(__file__).parents[1]
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

# Milvus vector DB
MILVUS_HOST = 'localhost'
MILVUS_PORT = default_server.listen_port

# OpenAI API
MAX_RETRIES = 3
OPENAI_GPT_MODEL = 'gpt-3.5-turbo'
OPENAI_EMBEDDING_MODEL = 'text-embedding-3-small'

# Logging
LOG_LVL = logging.INFO
SCRAPE_LOG_FN = LOG_DIR / "scrape.log"

# Politicians
POLITICIAN_ALIASES = {
    "Pedro Nuno Santos": [
        "PNS",
        "P.N.S.",
        "Pedro Nuno",
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
        "Ventura"
    ],
    "Rui Rocha": [
        "Rocha"
    ],
    "Mariana Mortágua": [
        "Mortágua",
        "coordenadora do BE",
        "coordenadora do Bloco de Esquerda",   
    ],
    "Paulo Raimundo": [
        "Raimundo",
        "secretário-geral do PCP"
    ],
    "Inês de Sousa Real": [
        "Inês Sousa Real",
        "Sousa Real",
        "porta voz do PAN",
        "porta voz do Partido Aniamis e Natureza",
    ],
    "Rui Tavares": [
        "Tavares",
        "líder do Livre",
        "líder do partido Livre",
    ],
}
POLITICIANS = list(POLITICIAN_ALIASES.keys())
PM_RESIGNATION_DATE = datetime(2023, 12, 7, 0, 0, 0)
