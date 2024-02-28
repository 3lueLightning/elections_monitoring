test_free:
	pytest -m "not openai"

test_openai:
	pytest -m "openai"
