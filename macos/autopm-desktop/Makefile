.PHONY: build
build: deps
	wails build

.PHONY: deps
deps:
	command -v wails > /dev/null || go install github.com/wailsapp/wails/v2/cmd/wails@latest

