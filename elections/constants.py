from pathlib import Path


# Folders
PACKAGE_ROOT = Path(__file__).parent
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
