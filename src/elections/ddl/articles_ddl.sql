CREATE TABLE "articles" (
    "article_id" INTEGER PRIMARY KEY AUTOINCREMENT,
    "title" TEXT,
    "description" TEXT,
    -- The publication date and time of the article
    "pubdate" TIMESTAMP,
    "publisher" TEXT,
    -- The Google URL where the full article can be found (then it redirects to the original article URL)
    "url" TEXT,
    "summary" TEXT,
    -- Keywords or tags associated with the article extracted via NLP with NLTK
    "keywords" TEXT,
    -- The full text content of the article
    "text" TEXT,
    -- The date and time when the article record was created in the database
    "creation_datetime" TIMESTAMP,
    -- Query used to obtain the article
    "query" TEXT
);
