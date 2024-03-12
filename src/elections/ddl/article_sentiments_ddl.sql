CREATE TABLE article_sentiments (
    sentiment_id INTEGER PRIMARY KEY AUTOINCREMENT,
    creation_datetime TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    article_id INTEGER,
    -- json containing a list with all the politicans mentiones in the article along with 
    -- their sentiment score (0 to 1, 1 being exteremely positive) and citations to back it up
    analysis TEXT,
    system_prompt TEXT,
    user_prompt TEXT,
    error_message TEXT,
    FOREIGN KEY (article_id) REFERENCES articles (article_id)
);