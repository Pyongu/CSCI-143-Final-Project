# Twitter Clone
[![](https://github.com/Pyongu/CSCI-143-Final-Project/actions/workflows/tests.yml/badge.svg)](https://github.com/Pyongu/CSCI-143-Final-Project/actions/workflows/tests.yml)
# Overview

This repository contains a simple Twitter clone — a CRUD web application built with Python, Flask, Jinja, PostgreSQL, Docker, Gunicorn, and Nginx. The project provides both development and production Docker containers, managed via a production-ready Docker Compose setup to streamline deployment and development workflows.

# Features

- **Home**: Paginated feed (20 messages/page)

- **Login/Logout**: Cookie-based session management

- **Create User**: Sign-up form with password confirmation

- **Create Message**: Authenticated message posting

- **Search**: Full-text search using PostgreSQL RUM index

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
