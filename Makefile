SOURCE= . app tests 
MAX_LINE_LENGTH=100

black:
	black -l $(MAX_LINE_LENGTH) $(SOURCE)

isort:
	isort -l $(MAX_LINE_LENGTH) $(SOURCE)
