SOURCE= *.py app tests
EXCLUDE= __pycache__ venv migrations .pytest_cache data
MAX_LINE_LENGTH=79

black:
	black -l $(MAX_LINE_LENGTH) $(SOURCE) --force-exclude $(EXCLUDE)

isort:
	isort -l $(MAX_LINE_LENGTH) --profile black $(SOURCE)

autoflake:
	autoflake $(SOURCE) -r --remove-all-unused-imports --in-place --remove-unused-variables 

quality: black autoflake isort