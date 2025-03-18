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

setup: ## 🎭 Setup poetry
	@echo "🎭 Setting up poetry..."
	@pip install -U pip setuptools
	@pip install poetry
	@poetry config virtualenvs.create false
	@poetry install

install: ## 📦 Install python packages
	@make clean-packages
	@echo "📦 Installing python packages..."
	@poetry install

lint: ## 🕵️‍♂️ Run python linter
	@echo "🕵️‍♂️ Running python linter..."
	@poetry run pyright

py-clean-cache: ## 🧹 Clean python cache
	@echo "🧹 Cleaning python cache..."
	@find . -type d -name __pycache__ -exec rm -r {} \+

chatbot: ## 🚀 Start the chatbot using sk
	@echo "🚀 Starting the chatbot using sk..."
	@poetry run python llm-workflow-orchestrator/ui.py --type chatbot

chatbot-agent: ## 🚀 Start the chatbot using sk-agent
	@echo "🚀 Starting the chatbot using sk-agent..."
	@poetry run python llm-workflow-orchestrator/ui.py --type agent

	