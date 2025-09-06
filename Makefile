# Makefile for Daily Equipment Inspection System

.PHONY: help install install-dev migrate createsuperuser runserver test clean lint format

help:  ## Show this help message
	@echo "Daily Equipment Inspection System - Available Commands:"
	@echo ""
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

install:  ## Install production dependencies
	pip install -r requirements.txt

install-dev:  ## Install development dependencies
	pip install -r requirements-dev.txt

migrate:  ## Run database migrations
	python manage.py makemigrations
	python manage.py migrate

load-data:  ## Load initial checklist items
	python manage.py load_checklist_items

createsuperuser:  ## Create Django superuser
	python manage.py createsuperuser

runserver:  ## Start development server
	python manage.py runserver

test:  ## Run tests
	python manage.py test

shell:  ## Open Django shell
	python manage.py shell

check:  ## Check for Django issues
	python manage.py check

collectstatic:  ## Collect static files
	python manage.py collectstatic --noinput

clean:  ## Clean Python cache files
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete

setup:  ## Complete project setup
	python setup.py

setup-dev:  ## Complete project setup with dev dependencies
	python setup.py --dev --create-superuser

# Development tools (requires requirements-dev.txt)
lint:  ## Run code linting
	flake8 .
	mypy .

format:  ## Format code
	black .
	isort .

# API commands
api-test:  ## Test API endpoints
	@echo "Testing API endpoints..."
	@echo "Admin: http://127.0.0.1:8000/admin/"
	@echo "API Root: http://127.0.0.1:8000/api/"
	@echo "Equipment: http://127.0.0.1:8000/api/equipment/"

# Database commands
reset-db:  ## Reset database (WARNING: This will delete all data!)
	@echo "⚠️  This will delete all data. Are you sure? [y/N]" && read ans && [ $${ans:-N} = y ]
	rm -f db.sqlite3
	python manage.py migrate
	python manage.py load_checklist_items

# Backup commands
backup-db:  ## Backup database
	python manage.py dumpdata --indent 2 > backup_$(shell date +%Y%m%d_%H%M%S).json

restore-db:  ## Restore database from backup (provide BACKUP_FILE=filename)
	python manage.py loaddata $(BACKUP_FILE)