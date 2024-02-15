import re


def escape_quotes_within_citation(text):
    def escape_quotes(match):
        citation_text = match.group(1)
        escaped_citation = citation_text.replace('"', r'\"')
        return f'"citation": "{escaped_citation}",'

    return re.sub(r'"citation": "(.*?)"\s*,', escape_quotes, text)
