MPY=python manage.py

lazy:
	$(MPY) makemigrations
	$(MPY) migrate

run:
	$(MPY) runserver

shell:
	$(MPY) shell
