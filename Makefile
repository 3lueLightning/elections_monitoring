install:
	pip install .

e-install:
	pip install -e .

dev-install:
	pip install -e '.[dev]'

test_free:
	pytest -m "not openai"

test_openai:
	pytest -m "openai"
