import os

from pathlib import Path

from milvus import default_server


# Folders
PACKAGE_ROOT = Path(__file__).parents[1]
SRC_FOLDER = PACKAGE_ROOT / "elections"
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
OPENAI_EMBEDDING_MODEL = 'text-embedding-3-small'

# Politicians
POLITICIANS = [
    "Pedro Nuno Santos",
    "Luís Montenegro",
    "André Ventura",
    "Rui Rocha",
    "Mariana Mortágua",
    "Paulo Raimundo",
    "Inês de Sousa Real",
    "Rui Tavares"
]
