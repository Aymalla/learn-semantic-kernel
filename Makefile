SHELL := /bin/bash

.PHONY: help backend-build search-dev search-start search-eval creation-start poetry-setup poetry-install py-lint py-clean-cache import-bwm-ca-certs load-test
.DEFAULT_GOAL := help
.ONESHELL: # Applies to every target in the file https://www.gnu.org/software/make/manual/html_node/One-Shell.html
MAKEFLAGS += --silent # https://www.gnu.org/software/make/manual/html_node/Silent.html

# Load environment file if exists
ENV_FILE := .env
ifeq ($(filter $(MAKECMDGOALS),config clean),)
	ifneq ($(strip $(wildcard $(ENV_FILE))),)
		ifneq ($(MAKECMDGOALS),config)
			include $(ENV_FILE)
			export
		endif
	endif
endif

help: ## 💬 This help message :)
	grep -E '[a-zA-Z_-]+:.*?## .*$$' $(firstword $(MAKEFILE_LIST)) | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-23s\033[0m %s\n\n", $$1, $$2}'

start-chatbot-sk: py-clean-cache ## 🚀 Start the chatbot
	@echo "🚀 Starting the chatbot..."
	@poetry run python ai-workflow-sk/main.py

start-chatbot-sk-agent: py-clean-cache ## 🚀 Start the chatbot using sk-agent
	@echo "🚀 Starting the chatbot..."
	@poetry run python ai-workflow-sk-agent/main.py

poetry-setup: ## 🎭 Setup poetry
	@echo "🎭 Setting up poetry..."
	@pip install -U pip setuptools
	@pip install poetry
	@poetry config virtualenvs.create false

poetry-install: ## 📦 Install python packages
	@make clean-packages
	@echo "📦 Installing python packages..."
	@poetry install

py-lint: ## 🕵️‍♂️ Run python linter
	@echo "🕵️‍♂️ Running python linter..."
	@poetry run pyright

py-clean-cache: ## 🧹 Clean python cache
	@echo "🧹 Cleaning python cache..."
	@find . -type d -name __pycache__ -exec rm -r {} \+

	