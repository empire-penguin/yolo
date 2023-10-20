export CURRENT_DIR = $(shell pwd)

# Set the name of your virtual environment
VENV_NAME = venv

# Set the path to your virtual environment
VENV_PATH = $(VENV_NAME)/bin

# Set the name of your main Python file
MAIN_FILE = main.py

# Set the name of your Python interpreter
PYTHON_INTERPRETER = python3

# Set the name of your requirements file
REQUIREMENTS_FILE = requirements.txt

# Create the virtual environment
venv:
	$(PYTHON_INTERPRETER) -m venv $(VENV_NAME)

# Activate the virtual environment
activate:
	source $(VENV_PATH)/activate

# Install dependencies
install:
	$(VENV_PATH)/pip install -r $(REQUIREMENTS_FILE)

# Run the main Python file
run:
	$(VENV_PATH)/$(PYTHON_INTERPRETER) $(MAIN_FILE)

# Test the utils Python file
test:
	$(VENV_PATH)/$(PYTHON_INTERPRETER) $(CURRENT_DIR)/tests/utils.py


