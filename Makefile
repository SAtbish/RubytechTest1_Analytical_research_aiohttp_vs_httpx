files_to_format ?= logger main.py
files_to_check ?= logger main.py

format_and_check: format check

format: remove_imports isort black docformatter

check: flake8 pylint ruff black_check docformatter_check bandit

remove_imports:
	autoflake -ir --remove-unused-variables \
		--ignore-init-module-imports \
		--remove-all-unused-imports \
		${files_to_format}


## Sort imports
isort:
	isort ${files_to_format}


## Format code
black:
	black ${files_to_format}


## Check code formatting
black_check:
	black --check ${files_to_check}


## Format docstring PEP 257
docformatter:
	docformatter -ir ${files_to_format}


## Check docstring formatting
docformatter_check:
	docformatter -cr ${files_to_check}


## Check code security
bandit:
	bandit -r ${files_to_check}


## Check pep8
flake8:
	flake8 ${files_to_check}

## Check google spec.
pylint:
	pylint ${files_to_check}

## Check pep8
ruff:
	ruff ${files_to_check}

## Check typing
mypy:
	mypy ${files_to_check}
