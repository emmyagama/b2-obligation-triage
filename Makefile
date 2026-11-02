ifeq ($(OS),Windows_NT)
PYTHON ?= py -3.11
else
PYTHON ?= $(shell command -v python3.11 2>/dev/null || command -v python3)
endif
.PHONY: setup test
setup:
	$(PYTHON) scripts/venv.py setup
test:
	$(PYTHON) scripts/venv.py test
