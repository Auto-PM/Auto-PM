# This file contains useful helpers.

.PHONY: lint
lint:
	./venv/bin/ruff check .
	./venv/bin/mypy

.PHONY: fmt
fmt:
	./venv/bin/ruff check --fix .

.PHONY: run
run: venv
	./venv/bin/uvicorn main:app --reload

.PHONY: ngrok-tunnel
ngrok-tunnel:
	command -v ngrok >/dev/null 2>&1 || (brew install ngrok)
	ngrok http 8000

venv: venv/bin/pip requirements.txt
	python3 -m venv venv
	./venv/bin/pip3 install wheel pip-tools
	touch venv

venv/bin/pip:
	python3 -m venv venv
	./venv/bin/pip3 install wheel pip-tools

requirements.txt: venv/bin/pip requirements.in
	./venv/bin/pip-compile --resolver=backtracking requirements.in
	./venv/bin/pip3 install -r requirements.txt
	./venv/bin/mypy --install-types

.PHONY: e2e-test
e2e-test: venv
	./test/e2e-test.sh

.PHONY: generate
generate: venv
	venv/bin/python3 -m gql_schema_codegen -p ./schemas/Linear-API@current.graphql -t linear_types.py

.PHONY: clean
clean:
	rm -rf ./venv

