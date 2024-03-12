tt = pd.DataFrame(
    [
        {"article_id": 1, "name": "Rui Rocha", "score": None, "quote": None},
        {"article_id": 1, "name": "Rui Rocha", "score": None, "quote": None},
        {"article_id": 1, "name": "Ines de Sousa Real", "score": None, "quote": None},
        {"article_id": 1, "name": "Ines de Sousa Real", "score": None, "quote": None},
        {"article_id": 1, "name": "Rui Rocha", "score": .4, "quote": "me"},
        {"article_id": 1, "name": "Rui Rocha", "score": .4, "quote": "you"},
        {"article_id": 2, "name": "Ines de Sousa Real", "score": None, "quote": None},
        {"article_id": 2, "name": "Ines de Sousa Real", "score": None, "quote": None},
        {"article_id": 2, "name": "Rui Rocha", "score": .6, "quote": "me"},
        {"article_id": 3, "name": "Rui Rocha", "score": None, "quote": None},
    ]
)
#tt.drop_duplicates(subset=["name"], keep="first")