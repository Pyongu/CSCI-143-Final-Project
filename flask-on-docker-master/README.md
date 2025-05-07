# Overview

This repo containerizes a Flask application using Docker, PostgreSQL, Gunicorn, and Nginx. PostgreSQL is used as the database to store structured data. Gunicorn serves as the WSGI HTTP server to manage Flask in a production environment. Nginx is used as a reverse proxy to handle incoming requests and improve performance. Docker is used to containerize all components, ensuring portability and easy deployment. Included is a production-ready Docker Compose file that adds Gunicorn and Nginx to handle static and media files.

![Gif](docker_flask_.gif)

# Build Instructions

**Setup**

You need to create a .env.prod and a .env.prod.db file in the root of your directory.

.env.prod
```
FLASK_APP=project/__init__.py
FLASK_DEBUG=0
DATABASE_URL=postgresql://<username>:<password>@db:5432/<dbname>
SQL_HOST=db
SQL_PORT=5432
DATABASE=postgres
APP_FOLDER=/home/app/web
```
.env.prod.db
```
POSTGRES_USER=<username>
POSTGRES_PASSWORD=<password>
POSTGRES_DB=<dbname>
```

**Development**

This command builds a new image and spins up the containers. If this command doesn't work, try running the last command first.
```
$ docker compose up -d --build
```
This command creates the SQL tables
```
$ docker compose exec web python manage.py create_db
```
This command  removes the volumes along with the containers
```
$ docker compose down -v
```

**Production**

This command builds a new image and spins up the containers. If this command doesn't work, try running the last command first.
```
$ docker compose -f docker-compose.prod.yml up -d --build
```
This command creates the SQL tables
```
$ docker compose -f docker-compose.prod.yml exec web python manage.py create_db
```
This command removes the volumes along with the containers
```
$ docker compose -f docker-compose.prod.yml down -v
```

# Portforwarding

In order to locally host your Flask application, you need to enable portforwarding. The default port for this repo is 5234 for development and 1447 for production. To enable the portforwarding make sure you add the following to your ssh command.

**Development**
```
$ ssh -L localhost:8080:10.253.1.15:5234
```
 **Production**
 ```
$ ssh -L localhost:8080:10.253.1.15:1447
 ```

# Uploading
The image can be uploaded at http://localhost:8080/upload

The image can be viewed at http://localhost:8080/media/IMAGE_FILE_NAME
