ifeq ($(shell [ -d $(HOME)/goinfre ] && echo 1), 1)

export UV_CACHE_DIR := $(HOME)/goinfre/.cache/uv
export HF_HOME := $(HOME)/goinfre/.cache/huggingface

endif

UV_PROJECT_ENVIRONMENT = ".venv"
PYTHON = $(UV_PROJECT_ENVIRONMENT)/bin/python3
PIP = $(UV_PROJECT_ENVIRONMENT)/bin/pip
UV = $(UV_PROJECT_ENVIRONMENT)/bin/uv

MYPY_FLAGS = --warn-return-any --warn-unused-ignores \
		--ignore-missing-imports --disallow-untyped-defs \
		--check-untyped-defs --explicit-package-bases \
		--namespace-packages

RM = rm -rf

install:
	@if [ ! -d $(UV_PROJECT_ENVIRONMENT) ]; then \
		python3 -m venv $(UV_PROJECT_ENVIRONMENT); \
	elif [ -d $(UV_PROJECT_ENVIRONMENT) ] && [ ! -x $(PYTHON) ]; then \
		python3 -m venv $(UV_PROJECT_ENVIRONMENT); \
	fi
	@if [ ! -x $(UV) ]; then \
		if [ ! -x $(PIP) ]; then \
			$(PYTHON) -m ensurepip; \
		fi; \
		$(PIP) install uv; \
	fi
	$(UV) sync

run: install
	$(UV) run python3 -m src $(ARGS)

debug: install
	$(PYTHON) pdb -m src $(ARGS)

clean:
	@$(RM) -rf */__pycache__
	@$(RM) -rf */*/__pycache__
	@$(RM) -rf .mypy_cache

destroy: clean
	@$(RM) $(UV_PROJECT_ENVIRONMENT)

lint: install
	clear
	$(PYTHON) -m flake8
	$(PYTHON) -m mypy $(MYPY_FLAGS) .

lint-strict: install
	clear
	$(PYTHON) -m flake8
	$(PYTHON) -m mypy --strict .

.PHONY: install run lint clean destroy lint-strict debug
