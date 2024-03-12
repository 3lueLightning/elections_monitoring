# Instructions to run sentiment analysis
The system is run in 3 consecutive steps:
1. **scrape news articles**:
    1. functions: 
        1. find articles online about each of the politicians (in the constants.py file)
        2. parse those files to obtain its: title, description, text (content)
        3. store it in a sqlite database (name defined in constants.NEWS_DB): articles table
    2. entry point: 1_articles_scraping.ipynb
2. **sentiment analysis**:
    1. functions:
        1. fetch articles in sqlite database (constants.NEWS_DB)
        2. use the chat completions API from OpenAI to run the sentiment analysis prompts defined in (elections.prompts.templates followed by user_prompt or system_prompt). It uses the article's title, description and text to build the user prompt from the user_prompt template.
        3. the instructor package patches the openAi API to enfornce that the result provided by the selected chat model (constants.OPENAI_GPT_MODEL) respects the required schema defined by the pydantic object ArticleSentiment (defined in elections.data_schemas)
        4. ArticleSentiment is json serialized and stored in a sqlite database (see constants.NEWS_DB): article_sentiments table
    2. entry point: 2_article_sentiments.ipynb
3. **results analysis**:
    1. function:
        1. explore, analyse and report the data generated via "sentiment analysis"
    2. entry point: 3_results_analysis.ipynb
