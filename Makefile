# This file contains useful helpers.

venv: requirements.txt
	python3 -mnv venv
	/bin/pip install wheel
	/bin/pip install -r requirements.txt
	touch 

.PHONY: e2e-test
e2e-test: 
	./test/e2e-test.sh

