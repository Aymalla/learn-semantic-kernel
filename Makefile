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

backend-build: ## 🔨 Build backend services
	@echo "🔨 Build backend services.."
	@./mvnw install -f backend 

search-dev: backend-build ## 🚀 Start the search service in dev mode
	@echo "🚀 Starting the search service..."
	@./mvnw quarkus:dev -Dquarkus.devservices.enabled=false -f backend/search

search-start: ## 🚀 Start the search service
	@echo "🚀 Starting the search service..."
	@./mvnw clean install -DskipTests -f backend && ./mvnw quarkus:dev -Dquarkus.devservices.enabled=false -f backend/search

search-eval: ## 🧪 Evaluate the search result
	@echo "🧪 Run search evaluation..."
	@sh ./evaluation/run_evaluate.sh

creation-start: ## 🚀 Start the creation 
	@make backend-build
	@echo "🚀 Starting the creation service..."
	@./mvnw quarkus:dev -f backend/creation

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

import-bwm-ca-certs: ## 📦 Import BWM CA certificate for TLS
	@echo "📦 Importing BWM CA certificate..."
	@CERTS_TEMP_DIR=./certs
	@OUTPUT_JKS_FILE=$CERTS_TEMP_DIR/BMW_Trusted_Certificates_Latest.jks
	@echo "🔑 Downloading latest BMW trusted certificates..."
	@mkdir -p $CERTS_TEMP_DIR
	@curl -o $OUTPUT_JKS_FILE http://sslcrl.bmwgroup.com/pki/BMW_Trusted_Certificates_Latest.jks
	@echo "🔑 Adding latest BMW certificates to your java keystore..."
	@keytool -importkeystore -noprompt -srckeystore $OUTPUT_JKS_FILE -srcstorepass changeit -destkeystore "${JAVA_HOME}/lib/security/cacerts"
	@rm -rf $CERTS_TEMP_DIR

load-test: ## 🚀 Start the load test
	@echo "🚀 Starting the load test..."
	@k6 run load-testing/search-tests.js
	