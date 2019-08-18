help:
	@echo '    init'
	@echo '        install pipenv and all project dependencies'
	@echo '    test'
	@echo '        run all tests'

init:
	@echo 'Install python dependencies'
	pip install pipenv
	pipenv install
	psql -c 'create database purbeurre_db;' -U postgres

test:
	@echo 'Run all tests'
	pipenv run python manage.py test --settings=purbeurre.settings.travis