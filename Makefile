# This file contains useful helpers.

.ve: requirements.txt
	python3 -m venv .ve
	.ve/bin/pip install wheel
	.ve/bin/pip install -r requirements.txt
	touch .ve

.PHONY: e2e-test
e2e-test: .ve
	./test/e2e-test.sh

