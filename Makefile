# This file contains useful helpers.

venv: requirements.txt
	python3 -m venv venv
	./venv/bin/pip3 install wheel
	./venv/bin/pip3 install -r requirements.txt

.PHONY: e2e-test
e2e-test: venv
	./test/e2e-test.sh

