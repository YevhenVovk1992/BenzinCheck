# Travel With Me - this is a travel service.
### Create your routes if you are professional guide. Or read-made itineraries if you want to relax or challenge yourself.
Link - 
___
![image](https://user-images.githubusercontent.com/104986485/200116448-9091b282-d132-45c1-836a-ca3c18842236.png)
___
### What we do?
Technologies used: Djando, Django Unittest, Django crispy forms, DjangoORM, MongoDB, SQLlite, Docker, Jinja2, JavaScripts, HTML5, CSS 

Create 3 models and form for them. These are routes, events and places. In Django, ORM created connections. Information about the stops along the route is stored in the database as a JSON file. It also stores information about users who are on the route. Full route information can only be viewed by registered users. Route, event and place can only be added by a user with the role of Guide. Confirmation on the fate of the campaign adds only the admin.
A registration system has been created for users in 2 roles - guide and traveler. The admin role can be obtained by a user in the admin panel and only from the admin.
HTML pages are dynamic, part of the information is hidden from unregistered users.
Unit Tests have been developed for this application.
___
### How to start project?
1. pip install -r requerements.txt;
2. Create .env file and write to it enviroment variables:
	- SECRET_KEY
	- MONGO_CONNECTION_STRING ('mongodb://user:password@host:port')
	- MONGO_INITDB_ROOT_USERNAME
	- MONGO_INITDB_ROOT_PASSWORD
3. Run 'docker-compose up -d';
4. Run 'python manage.py migrate';
5. Create superuser 'python manage.py createsuperuser' and add user's groups: guide and traveler in admin panel;

