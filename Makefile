.PHONY: help install test lint format clean all docker-build docker-test docker-clean

# Default target
help:
	@echo "Available commands:"
	@echo ""
	@echo "Local:"
	@echo "  make install         - Install all dependencies with uv"
	@echo "  make test            - Run all tests"
	@echo "  make test-ui         - Run tests in UI mode"
	@echo "  make test-headless   - Run tests in headless mode"
	@echo "  make test-html       - Run tests and generate HTML report"
	@echo "  make lint            - Run ruff linter"
	@echo "  make format          - Format code with ruff"
	@echo "  make format-check    - Check code formatting"
	@echo "  make fix             - Auto-fix all linting issues"
	@echo "  make clean           - Clean temporary files"
	@echo "  make all             - Install, format, lint and test"
	@echo ""
	@echo "Docker:"
	@echo "  make docker-build    - Build Docker image"
	@echo "  make docker-test    - Run tests in Docker (headless)"
	@echo "  make docker-test-html - Run tests in Docker with HTML report"
	@echo "  make docker-shell    - Open shell in Docker container"
	@echo "  make docker-clean    - Remove Docker containers and images"

# Install dependencies
install:
	@echo "Installing dependencies with uv..."
	uv sync

# Run tests
test:
	@mkdir -p logs
	uv run python -m pytest tests/ -v

test-ui:
	@mkdir -p logs
	HEADLESS=ui uv run python -m pytest tests/ -v

test-headless:
	@mkdir -p logs
	HEADLESS=headless uv run python -m pytest tests/ -v

test-html:
	@mkdir -p reports logs
	rm -rf reports/* 2>/dev/null || true
	uv run python -m pytest tests/ -v --html=reports/test_report.html --self-contained-html

# Linter
lint:
	@echo "Running ruff check..."
	uv run ruff check pages/ tests/ utils/ data/ locators/

# Format code
format:
	@echo "Formatting code with ruff..."
	uv run ruff format pages/ tests/ utils/ data/ locators/

format-check:
	@echo "Checking code formatting..."
	uv run ruff format --check pages/ tests/ utils/ data/ locators/

# Auto-fix issues
fix:
	@echo "Auto-fixing linting issues..."
	uv run ruff check --fix pages/ tests/ utils/ data/ locators/
	@echo "Formatting code..."
	uv run ruff format pages/ tests/ utils/ data/ locators/

# Clean temporary files
clean:
	@echo "Cleaning temporary files..."
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name "*.egg-info" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	rm -rf .mypy_cache
	rm -rf htmlcov
	rm -rf .coverage
	rm -rf .ruff_cache
	rm -rf .vscode
	rm -rf reports
	rm -rf logs
	@echo "Cleanup complete!"

# Run all checks
all: install format lint test
	@echo "All checks passed!"

# Docker commands
docker-build:
	@echo "Building Docker image..."
	docker-compose build

docker-test:
	@echo "Running tests in Docker (headless)..."
	@mkdir -p logs
	docker-compose run --rm -v $(CURDIR)/logs:/app/logs tests uv run python -m pytest tests/ -v

docker-test-html:
	@echo "Running tests in Docker with HTML report..."
	@mkdir -p logs reports
	rm -rf reports/* 2>/dev/null || true
	docker-compose run --rm -v $(CURDIR)/logs:/app/logs -v $(CURDIR)/reports:/app/reports tests uv run python -m pytest tests/ -v --html=reports/test_report.html --self-contained-html

docker-shell:
	@echo "Opening shell in Docker container..."
	@mkdir -p logs
	docker-compose run --rm -v $(CURDIR)/logs:/app/logs tests /bin/bash

docker-clean:
	@echo "Cleaning Docker containers and images..."
	docker-compose down
	docker-compose rm -f
	docker rmi saucedemo_ui_tests_selenium-tests 2>/dev/null || true
	docker rmi saucedemo_ui_tests_selenium-tests-ui 2>/dev/null || true
	@echo "Docker cleanup complete!"
