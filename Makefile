SHELL := /bin/bash
PYTHON = python3
TEST_PATH = ./tests/
init:
	@pip install --upgrade pip
	@pip install -e .
	#@pip install -r requirements.txt -U   #we need this explicit variant wheb using unreleased -e dependencies - to keep automatic testing happy

init-dev: init
	@pip install -e .[dev]

test:
	@${PYTHON} -m pytest ${TEST_PATH} --disable-warnings