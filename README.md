# BenzinCheck
### Get information about the price of fuel for your region or country. Use for it our websuite or REST API service.
Link - 
___

___
### What we do?
Technologies used: Djando, Django Unittest, Django crispy forms, DjangoORM, Celery Worker, PostgresDB, Docker, Jinja2, HTML5, CSS 

Create Djngo project with Celery Worker (used RabbitMQ as broker). 
___
### How to start project?
1. pip install -r requerements.txt;
2. Create .env file and write to it enviroment variables:
	- SECRET_KEY
	- POSTGRES_USER
	- POSTGRES_PASSWORD
	- POSTGRES_DB
	- DB_HOST
	- DB_PORT
	- CELERY_BROKER_URL (pyamqp://guest@localhost//)
3. Run 'docker-compose up -d';
4. Run 'python manage.py migrate';
5. Create superuser 'python manage.py createsuperuser' and add user's groups: guide and traveler in admin panel;
6. Run Celery Worker - python -m celery -A BenzinCheck worker;

