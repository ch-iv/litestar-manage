# Variables
PYTHON := pdm run python
PYTEST := pdm run pytest
RUFF := pdm run ruff format
FIND := find

# Directories
SRC_DIR := src
TEST_DIR := tests

# Targets
.PHONY: clean test run

	
#Format the files
format:
	$(RUFF) $(SRC_DIR)
	$(RUFF) $(TEST_DIR)

# Clean target to delete __pycache__ directories
clean:
	$(FIND) . -type d -name "__pycache__" -exec rm -rf {} +

test:
	$(PYTEST) $(TEST_DIR) -vv -s --showlocals
